from fastapi import APIRouter, Depends, HTTPException
from fastapi import Body
from typing import List

from app.models.stock_query import StockQuery
from app.models.stock import Stock
from app.services.stock_service import get_stocks_service
from app.utils.mcp_response import mcp_response

from app.services.stock_service import get_stocks_service, upload_stocks_service

router = APIRouter()

@router.get("/stocks")
@mcp_response
async def get_stocks(query: StockQuery = Depends()):
    return await get_stocks_service(query)

@router.post("/stocks/upload")
async def upload_stocks_csv(stocks: List[Stock] = Body(...)):
    return await upload_stocks_service(stocks)