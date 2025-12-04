from typing import List
from pydantic import BaseModel

from app.domain.models.user_data import Stock


class AddOrUpdateUserRequest(BaseModel):
    stocks: List[Stock]
