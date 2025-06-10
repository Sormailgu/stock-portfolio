from fastapi import APIRouter, Depends, HTTPException
from app.models.stock_query import StockQuery
from app.services.stock_service import get_stocks_service
from app.utils.mcp_response import mcp_response

router = APIRouter()

@router.get("/stocks")
@mcp_response
async def get_stocks(query: StockQuery = Depends()):
    return await get_stocks_service(query)