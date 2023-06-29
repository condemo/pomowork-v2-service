from pydantic import BaseModel
from typing import Optional
from datetime import date


class CardCreate(BaseModel):
    project_id: int
    pomo_count: Optional[int] = 0
    price_per_hour: Optional[float] = None
    total_price: Optional[float] = None
    collected: Optional[bool] = False


class CardUpdate(CardCreate):
    id: int


class CardResponse(CardCreate):
    id: int
    created_at: date

    class Config:
        orm_mode = True
