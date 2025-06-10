from fastapi import APIRouter, Depends, HTTPException
from app.models.stock_query import StockQuery
from app.services.stock_service import get_stocks_service
from app.utils.mcp_response import mcp_response

router = APIRouter()

@router.get("/stocks")
@mcp_response
async def get_stocks(query: StockQuery = Depends()):
    return await get_stocks_service(query)


CSV_FILE_PATH = "data/stocks.csv"

@router.post("/stocks/upload")
async def upload_stocks_csv(stocks: List[Stock] = Body(...)):
    if not stocks:
        raise HTTPException(status_code=400, detail="No stock records provided.")
    try:
        # Write to CSV
        with open(CSV_FILE_PATH, "w", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=Stock.__fields__.keys())
            writer.writeheader()
            for stock in stocks:
                writer.writerow(stock.dict())
        return {"message": "CSV file updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update CSV: {str(e)}")
