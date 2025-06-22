from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.responses import JSONResponse
from typing import List

from app.models.stock_query import StockQuery
from app.models.stock import Stock
from app.utils.response import api_response
from app.services.stock_service import (
    get_stocks_service,
    update_stocks_service,
    delete_stock_service,
)

router = APIRouter()

@router.get("/stocks")
async def get_stocks(query: StockQuery = Depends()):
    try:
        data = await get_stocks_service(query)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=api_response(
                status="success",
                code=200,
                message="Stocks retrieved successfully.",
                data=data,
            ),
        )
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=api_response(
                status="fail",
                code=e.status_code,
                message="",
                errors={"detail": e.detail},
            ),
        )

@router.post("/stocks/update")
async def update_stocks_csv(stocks: List[Stock] = Body(...)):
    try:
        result = await update_stocks_service(stocks)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=api_response(
                status="success",
                code=200,
                message=result.get("message", "Stocks updated successfully."),
                data=[],
            ),
        )
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=api_response(
                status="fail",
                code=e.status_code,
                message="",
                errors={"detail": e.detail},
            ),
        )

@router.delete("/stocks/{symbol}")
async def delete_stock(symbol: str):
    if not symbol:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=api_response(
                status="fail",
                code=400,
                message="",
                errors={"symbol": "Symbol is required"},
            ),
        )
    try:
        result = await delete_stock_service(symbol)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=api_response(
                status="success",
                code=200,
                message=result.get("message", "Stock deleted successfully."),
                data=[],
            ),
        )
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=api_response(
                status="fail",
                code=e.status_code,
                message="",
                errors={"detail": e.detail},
            ),
        )