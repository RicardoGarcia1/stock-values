from abc import ABC, abstractmethod
from typing import List

from app.domain.models.user_data import History, User


class EmailSenderPort(ABC):
    @abstractmethod
    def send_email(self, total: str, name: str, email:str , user_history: List[History]):
        pass
