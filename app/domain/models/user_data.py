from enum import Enum
from typing import List
from pydantic import BaseModel

class Currency(str, Enum):
    USD = "USD"  # Dólar estadounidense
    EUR = "EUR"  # Euro
    GBP = "GBP"  # Libra esterlina
    JPY = "JPY"  # Yen japonés
    CHF = "CHF"  # Franco suizo
    CAD = "CAD"  # Dólar canadiense
    AUD = "AUD"  # Dólar australiano

class Stock(BaseModel):
    amount: float
    index: str
    currency: Currency | None = Currency.EUR
    
class History(BaseModel):
    day: str
    totalValue: float

class UserPortfolio(BaseModel):
    name: str
    stocks: List[Stock]
    history: List[History] | None = None  

class UsersInfo(BaseModel):
    users_info: List[UserPortfolio]