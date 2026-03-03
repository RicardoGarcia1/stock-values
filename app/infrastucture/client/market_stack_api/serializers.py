from datetime import datetime
from typing import List
from pydantic import BaseModel

class Pagination(BaseModel):
    limit: int
    offset: int
    count: int
    total: int 


class Data(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: float
    adj_high: float | None = None
    adj_low: float | None = None
    adj_close: float | None = None
    adj_open: float | None = None
    adj_volume: float | None = None
    split_factor: int | None = None
    dividend: float | None = None
    symbol: str | None = None
    exchange: str | None = None
    date: datetime


class StockDetails(BaseModel):
    pagination:  Pagination
    data: List[Data]
    