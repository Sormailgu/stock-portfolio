from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os
import requests
from requests.exceptions import RequestException
from werkzeug.serving import make_server
import time

app = Flask(__name__)
CORS(app)

# Alpha Vantage API key (replace with your own key)
ALPHA_VANTAGE_API_KEY = "DJA0HOM47XGJWBCO"  # Replace with your Alpha Vantage API key
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

# Cache to store API results and avoid redundant calls
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
                    # Fetch company name using OVERVIEW endpoint
                    overview_url = f"{ALPHA_VANTAGE_BASE_URL}?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
                    overview_response = requests.get(overview_url, timeout=10)
                    
                    if overview_response.status_code != 200:
                        return jsonify({'error': f'Failed to fetch data for {symbol} from Alpha Vantage'}), 500
                    
                    overview_data = overview_response.json()
                    if not overview_data or 'Name' not in overview_data:
                        return jsonify({'error': f'No company data found for {symbol}'}), 404
                    
                    company = overview_data['Name']
                    
                    # Fetch current price using GLOBAL_QUOTE endpoint
                    quote_url = f"{ALPHA_VANTAGE_BASE_URL}?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
                    quote_response = requests.get(quote_url, timeout=10)
                    
                    if quote_response.status_code != 200:
                        return jsonify({'error': f'Failed to fetch price for {symbol} from Alpha Vantage'}), 500
                    
                    quote_data = quote_response.json()
                    if not quote_data or 'Global Quote' not in quote_data or '05. price' not in quote_data['Global Quote']:
                        return jsonify({'error': f'No price data found for {symbol}'}), 404
                    
                    price = float(quote_data['Global Quote']['05. price'])
                    
                    # Cache the results
                    cache[symbol] = (company, price)
                    
                    # Respect Alpha Vantage rate limits (5 calls per minute)
                    time.sleep(12)  # Wait 12 seconds between calls (5 calls/min = 1 call every 12s)
                
                except RequestException as e:
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
    # Create a server with a custom timeout
    server = make_server('0.0.0.0', 5000, app)
    server.timeout = 180  # Set timeout to 3 minutes (180 seconds)
    server.serve_forever()