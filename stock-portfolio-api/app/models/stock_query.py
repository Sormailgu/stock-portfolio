from pydantic import BaseModel
from typing import Optional

class StockQuery(BaseModel):
    fields: Optional[str] = "market,symbol,company,sector,industry,currency,shares,avgCost,currentPrice"
    market: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    sort_by: Optional[str] = None