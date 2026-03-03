from typing import List
from pydantic import BaseModel, EmailStr

from app.domain.models.user_data import Stock


class AddOrUpdateUserRequest(BaseModel):
    name: str | None = None
    stocks: List[Stock]
    user_identifier: str | None = None
    email : EmailStr | None = None
