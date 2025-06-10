import pandas as pd
import os
import yfinance as yf
from fastapi import HTTPException
from app.models.stock_query import StockQuery
from app.utils.cache import cache
import logging

logger = logging.getLogger(__name__)

async def get_stocks_service(query: StockQuery):
    file_path = 'data/stocks.csv'
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail='stocks.csv not found')
    df = pd.read_csv(file_path)
    logger.debug(f"Received query parameters: {query.model_dump()}")
    fields = query.fields.split(',')
    market_filter = query.market
    sector_filter = query.sector
    industry_filter = query.industry
    sort_by = query.sort_by
    companies, sectors, industries, current_prices = [], [], [], []
    for symbol in df['symbol']:
        if symbol in cache:
            company, price, sector, industry = cache[symbol]
        else:
            try:
                stock = yf.Ticker(symbol)
                info = stock.info
                company = info.get('longName', None)
                if not company:
                    raise HTTPException(status_code=404, detail=f'No company data found for {symbol}')
                sector = info.get('sector', 'N/A')
                industry = info.get('industry', 'N/A')
                price_data = stock.history(period='1d')
                if price_data.empty or 'Close' not in price_data.columns:
                    raise HTTPException(status_code=404, detail=f'No price data found for {symbol}')
                price = round(float(price_data['Close'].iloc[-1]), 2)
                cache[symbol] = (company, price, sector, industry)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f'Failed to fetch data for {symbol}: {str(e)}')
        companies.append(company)
        sectors.append(sector)
        industries.append(industry)
        current_prices.append(price)
    df['company'] = companies
    df['sector'] = [s.strip() for s in sectors]
    df['industry'] = [i.strip() for i in industries]
    df['currentPrice'] = current_prices
    logger.debug(f"DataFrame before filtering: {df.to_dict(orient='records')}")
    if market_filter:
        df = df[df['market'] == market_filter]
    if sector_filter:
        df = df[df['sector'] == sector_filter]
    if industry_filter:
        df = df[df['industry'] == industry_filter]
    if sort_by and sort_by in df.columns:
        df = df.sort_values(by=sort_by)
        logger.debug(f"After sorting by '{sort_by}': {df.to_dict(orient='records')}")
    valid_fields = [f for f in fields if f in df.columns]
    if not valid_fields:
        raise HTTPException(status_code=400, detail='No valid fields specified')
    df = df[valid_fields]
    logger.debug(f"Final DataFrame: {df.to_dict(orient='records')}")
    return df.to_dict(orient='records')