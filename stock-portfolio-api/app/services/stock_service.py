import csv
import pandas as pd
import yfinance as yf
from fastapi import HTTPException
from typing import List, Dict, Any
from app.models.stock_query import StockQuery
from app.models.stock import Stock
from app.utils.cache import cache
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

async def get_stocks_service(query: StockQuery) -> List[Dict[str, Any]]:
    file_path = settings.CSV_FILE_PATH
    if not file_path:
        raise HTTPException(status_code=500, detail='CSV file path is not configured')
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='CSV file not found')

    logger.debug(f"Received query parameters: {query.model_dump()}")
    fields = [f.strip() for f in query.fields.split(',')]
    filters = {
        'market': query.market,
        'sector': query.sector,
        'industry': query.industry
    }
    sort_by = query.sort_by

    # Fetch and cache company info and prices
    def fetch_info(symbol):
        if symbol in cache:
            return cache[symbol]
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            company = info.get('longName')
            if not company:
                raise ValueError('No company data')
            sector = info.get('sector', 'N/A')
            industry = info.get('industry', 'N/A')
            price_data = stock.history(period='1d')
            if price_data.empty or 'Close' not in price_data.columns:
                raise ValueError('No price data')
            price = round(float(price_data['Close'].iloc[-1]), 2)
            cache[symbol] = (company, price, sector, industry)
            return company, price, sector, industry
        except Exception as e:
            logger.error(f"Failed to fetch data for {symbol}: {e}")
            raise HTTPException(status_code=500, detail=f'Failed to fetch data for {symbol}: {str(e)}')

    companies, prices, sectors, industries = [], [], [], []
    for symbol in df['symbol']:
        company, price, sector, industry = fetch_info(symbol)
        companies.append(company)
        prices.append(price)
        sectors.append(sector.strip())
        industries.append(industry.strip())

    df['company'] = companies
    df['sector'] = sectors
    df['industry'] = industries
    df['currentPrice'] = prices

    # Apply filters
    for key, value in filters.items():
        if value:
            df = df[df[key] == value]

    # Sort if needed
    if sort_by and sort_by in df.columns:
        df = df.sort_values(by=sort_by)
        logger.debug(f"After sorting by '{sort_by}': {df.to_dict(orient='records')}")

    valid_fields = [f for f in fields if f in df.columns]
    if not valid_fields:
        raise HTTPException(status_code=400, detail='No valid fields specified')
    df = df[valid_fields]
    logger.debug(f"Final DataFrame: {df.to_dict(orient='records')}")
    return df.to_dict(orient='records')

async def update_stocks_service(stocks: List[Stock]) -> Dict[str, str]:
    file_path = settings.CSV_FILE_PATH
    if not stocks:
        raise HTTPException(status_code=400, detail='No stock records provided')
    try:
        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            df = pd.DataFrame(columns=list(Stock.__fields__.keys()))

        stock_dicts = [s.dict() if isinstance(s, Stock) else dict(s) for s in stocks]
        new_df = pd.DataFrame(stock_dicts)

        # Merge the existing and new stock records based on 'market' and 'symbol' as composite keys.
        # 1. Set both DataFrames' indexes to ['market', 'symbol'] to align records for update.
        # 2. Use df.update(new_df) to update existing records in df with values from new_df where keys match.
        # 3. Concatenate df with any new records from new_df that do not exist in df (i.e., new stocks).
        # 4. Reset the index to default integer index for easier downstream processing.
        df.set_index(['market', 'symbol'], inplace=True, drop=False)
        new_df.set_index(['market', 'symbol'], inplace=True, drop=False)
        df.update(new_df)
        combined = pd.concat([df, new_df[~new_df.index.isin(df.index)]])
        combined = combined.reset_index(drop=True)

        # Ensure correct column order
        fieldnames = list(Stock.__fields__.keys())
        combined = combined[fieldnames]
        combined.to_csv(file_path, index=False)

        logger.info(f"CSV file '{file_path}' updated successfully with {len(combined)} records.")
        return {"message": "CSV file updated successfully."}
    except Exception as e:
        logger.error(f"Failed to update CSV: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update CSV: {str(e)}")

async def delete_stock_service(symbol: str) -> Dict[str, str]:
    file_path = settings.CSV_FILE_PATH
    try:
        df = pd.read_csv(file_path)
        if symbol not in df['symbol'].values:
            raise HTTPException(status_code=404, detail=f'Stock with symbol {symbol} not found')
        df = df[df['symbol'] != symbol]
        df.to_csv(file_path, index=False)
        logger.info(f"Stock with symbol '{symbol}' deleted successfully.")
        return {"message": f"Stock with symbol '{symbol}' deleted successfully."}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='CSV file not found')
    except Exception as e:
        logger.error(f"Failed to delete stock: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete stock: {str(e)}")