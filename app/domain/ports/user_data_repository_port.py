from typing import List
from abc import ABC, abstractmethod

from app.domain.models.user_data import Stock, User

class UserDataRepositoryPort(ABC):
    @abstractmethod
    def add_user(self, new_user: User):
        pass

    @abstractmethod
    def delete_user(self, user_id: str):
        pass

    @abstractmethod
    def patch_user(self, user_to_update: User):
        pass
    
    @abstractmethod
    def get_stocks_by_user(self, user_id: str) -> List[Stock]:
        pass

    @abstractmethod
    def add_or_update_history_record(self, total:str, user_id: str):
        pass

    @abstractmethod
    def get_user_email_and_history(self, user_id:str):
        pass
    