from pydantic import BaseModel
from typing import Union

class Stock(BaseModel):
    market: str
    symbol: str
    currency: str
    shares: int
    avgCost: float