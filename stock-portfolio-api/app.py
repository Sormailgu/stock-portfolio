from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
import yfinance as yf
from functools import wraps
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

# Cache to store yfinance results
cache = {}

def mcp_response(f):
    """MCP decorator to standardize API responses for LLM consumption."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Execute the endpoint function
            result = f(*args, **kwargs)
            
            # Standard MCP response structure
            response = {
                "data": result if isinstance(result, list) else [],
                "metadata": {
                    "request_id": str(uuid.uuid4()),
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "success",
                    "endpoint": request.path,
                    "query_params": request.args.to_dict()
                },
                "errors": []
            }
            return jsonify(response), 200
        except Exception as e:
            # Handle errors with MCP structure
            response = {
                "data": [],
                "metadata": {
                    "request_id": str(uuid.uuid4()),
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "error",
                    "endpoint": request.path,
                    "query_params": request.args.to_dict()
                },
                "errors": [{"message": str(e), "code": 500}]
            }
            return jsonify(response), 500
    return decorated_function

@app.route('/api/stocks', methods=['GET'])
@mcp_response
def get_stocks():
    file_path = 'stocks.csv'
    
    # Check if CSV file exists
    if not os.path.exists(file_path):
        raise Exception('stocks.csv not found')
    
    # Read CSV file
    df = pd.read_csv(file_path)
    
    # Get query parameters for context
    fields = request.args.get('fields', 'market,symbol,company,sector,industry,currency,shares,avgCost,currentPrice').split(',')
    sector_filter = request.args.get('sector', None)
    industry_filter = request.args.get('industry', None)
    sort_by = request.args.get('sort_by', None)
    
    # Initialize lists for stock data
    companies = []
    sectors = []
    industries = []
    current_prices = []
    
    for symbol in df['symbol']:
        # Check cache first
        if symbol in cache:
            company, price, sector, industry = cache[symbol]
        else:
            try:
                # Fetch stock data using yfinance
                stock = yf.Ticker(symbol)
                info = stock.info
                
                # Get company name
                company = info.get('longName', None)
                if not company:
                    raise Exception(f'No company data found for {symbol}')
                
                # Extract sector and industry
                sector = info.get('sector', 'N/A')
                industry = info.get('industry', 'N/A')
                
                # Get current price
                price_data = stock.history(period='1d')
                if price_data.empty or 'Close' not in price_data.columns:
                    raise Exception(f'No price data found for {symbol}')
                price = round(float(price_data['Close'].iloc[-1]), 2)
                
                # Cache the results
                cache[symbol] = (company, price, sector, industry)
            
            except Exception as e:
                raise Exception(f'Failed to fetch data for {symbol}: {str(e)}')
        
        companies.append(company)
        sectors.append(sector)
        industries.append(industry)
        current_prices.append(price)
    
    # Add data to DataFrame
    df['company'] = companies
    df['sector'] = sectors
    df['industry'] = industries
    df['currentPrice'] = current_prices
    
    # Apply filters
    if sector_filter:
        df = df[df['sector'] == sector_filter]
    if industry_filter:
        df = df[df['industry'] == industry_filter]
    
    # Apply sorting
    if sort_by in df.columns:
        df = df.sort_values(by=sort_by)
    
    # Select requested fields
    valid_fields = [f for f in fields if f in df.columns]
    if not valid_fields:
        raise Exception('No valid fields specified')
    df = df[valid_fields]
    
    # Convert to JSON
    return df.to_dict(orient='records')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)