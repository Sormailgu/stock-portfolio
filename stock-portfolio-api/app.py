from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os
import yfinance as yf

app = Flask(__name__)
CORS(app)

# Cache to store yfinance results and avoid redundant calls
cache = {}

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    file_path = 'stocks.csv'
    
    # Check if CSV file exists
    if not os.path.exists(file_path):
        return jsonify({'error': 'stocks.csv not found'}), 404
    
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Initialize lists to store company names and current prices
        companies = []
        current_prices = []
        
        for symbol in df['symbol']:
            # Check cache first
            if symbol in cache:
                company, price = cache[symbol]
            else:
                try:
                    # Fetch stock data using yfinance
                    stock = yf.Ticker(symbol)
                    info = stock.info
                    
                    # Get company name
                    company = info.get('longName', None)
                    if not company:
                        return jsonify({'error': f'No company data found for {symbol}'}), 404
                    
                    # Get current price from the latest available data
                    price_data = stock.history(period='1d')
                    if price_data.empty or 'Close' not in price_data.columns:
                        return jsonify({'error': f'No price data found for {symbol}'}), 404
                    price = round(float(price_data['Close'].iloc[-1]), 2)
                    
                    # Cache the results
                    cache[symbol] = (company, price)
                
                except Exception as e:
                    return jsonify({'error': f'Failed to fetch data for {symbol}: {str(e)}'}), 500
            
            companies.append(company)
            current_prices.append(price)
        
        # Add company and currentPrice to DataFrame
        df['company'] = companies
        df['currentPrice'] = current_prices
        
        # Reorder columns to match desired output
        df = df[['market', 'symbol', 'company', 'currency', 'shares', 'avgCost', 'currentPrice']]
        
        # Convert to JSON
        data = df.to_dict(orient='records')
        return jsonify(data)
    
    except Exception as e:
        return jsonify({'error': f'Failed to process request: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)