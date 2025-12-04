from abc import ABC, abstractmethod

from app.domain.models.user_data import Stock


class StockApiPort(ABC): 
    @abstractmethod 
    async def get_price_eof(self, index: str) -> Stock:
        raise NotImplementedError

 