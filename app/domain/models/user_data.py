from decimal import Decimal
from enum import Enum
from typing import List
from pydantic import BaseModel

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    CHF = "CHF"
    CAD = "CAD"
    AUD = "AUD"


class Stock(BaseModel):
    amount: Decimal | None = Decimal("0")
    index: str
    currency: Currency | None = Currency.EUR


class History(BaseModel):
    day: str
    totalValue: Decimal


class User(BaseModel):
    name: str | None = None
    email: str | None = None
    user_identifier: str | None = None
    stocks: List[Stock]
    history: List[History] | None = None  




