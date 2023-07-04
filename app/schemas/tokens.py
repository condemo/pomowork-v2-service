from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: int
    token_type: int


class TokenData(BaseModel):
    id: Optional[int] = None
