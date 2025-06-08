from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import yfinance as yf
from functools import wraps
from datetime import datetime
import uuid
from pydantic import BaseModel
from typing import Optional, List
from fastapi.responses import JSONResponse
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache to store yfinance results
cache = {}

# Pydantic model for query parameters
class StockQuery(BaseModel):
    fields: Optional[str] = "market,symbol,company,sector,industry,currency,shares,avgCost,currentPrice"
    market: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    sort_by: Optional[str] = None

def mcp_response(f):
    """MCP decorator to standardize API responses for LLM consumption."""
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        try:
            # Execute the endpoint function
            result = await f(*args, **kwargs)
            
            # Standard MCP response structure
            response = {
                "data": result if isinstance(result, list) else [],
                "metadata": {
                    "request_id": str(uuid.uuid4()),
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "success",
                    "endpoint": f.__name__,
                    "query_params": kwargs.get('query', StockQuery()).dict() if hasattr(kwargs.get('query', StockQuery()), 'dict') else {}
                },
                "errors": []
            }
            return JSONResponse(content=response, status_code=200)
        except Exception as e:
            # Handle errors with MCP structure
            response = {
                "data": [],
                "metadata": {
                    "request_id": str(uuid.uuid4()),
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "error",
                    "endpoint": f.__name__,
                    "query_params": kwargs.get('query', StockQuery()).dict() if hasattr(kwargs.get('query', StockQuery()), 'dict') else {}
                },
                "errors": [{"message": str(e), "code": 500}]
            }
            return JSONResponse(content=response, status_code=500)
    return decorated_function

@app.get("/api/stocks")
@mcp_response
async def get_stocks(query: StockQuery = Depends()):
    file_path = 'stocks.csv'
    
    # Check if CSV file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail='stocks.csv not found')
    
    # Read CSV file
    df = pd.read_csv(file_path)
    
    # Log query parameters
    logger.debug(f"Received query parameters: {query.dict()}")
    
    # Get query parameters for context
    fields = query.fields.split(',')
    market_filter = query.market if query.market else None
    sector_filter = query.sector if query.sector else None
    industry_filter = query.industry if query.industry else None
    sort_by = query.sort_by
    
    # Initialize lists for stock data
    companies = []
    sectors = []
    industries = []
    current_prices = []
    
    for symbol in df['symbol']:
        #Check cache first
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
                    raise HTTPException(status_code=404, detail=f'No company data found for {symbol}')
                
                # Extract sector and industry
                sector = info.get('sector', 'N/A')
                industry = info.get('industry', 'N/A')
                
                # Get current price
                price_data = stock.history(period='1d')
                if price_data.empty or 'Close' not in price_data.columns:
                    raise HTTPException(status_code=404, detail=f'No price data found for {symbol}')
                price = round(float(price_data['Close'].iloc[-1]), 2)
                
                # Cache the results
                cache[symbol] = (company, price, sector, industry)
            
            except Exception as e:
                raise HTTPException(status_code=500, detail=f'Failed to fetch data for {symbol}: {str(e)}')
        
        companies.append(company)
        sectors.append(sector)
        industries.append(industry)
        current_prices.append(price)
    
    # Add data to DataFrame
    df['company'] = companies
    df['sector'] = [s.strip() for s in sectors]
    df['industry'] = [i.strip() for i in industries]
    df['currentPrice'] = current_prices
    
    # Log DataFrame before filtering
    logger.debug(f"DataFrame before filtering: {df.to_dict(orient='records')}")
    
    # Apply filters
    if market_filter:
        df = df[df['market'] == market_filter]    
    if sector_filter:
        df = df[df['sector'] == sector_filter]
    if industry_filter:
        df = df[df['industry'] == industry_filter]
    
    # Apply sorting
    if sort_by and sort_by in df.columns:
        df = df.sort_values(by=sort_by)
        logger.debug(f"After sorting by '{sort_by}': {df.to_dict(orient='records')}")
    
    # Select requested fields
    valid_fields = [f for f in fields if f in df.columns]
    if not valid_fields:
        raise HTTPException(status_code=400, detail='No valid fields specified')
    df = df[valid_fields]
    
    # Log final DataFrame
    logger.debug(f"Final DataFrame: {df.to_dict(orient='records')}")
    
    # Convert to JSON
    return df.to_dict(orient='records')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5001)