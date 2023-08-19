from pydantic import BaseModel
from typing import Optional
from datetime import date


class CardCreate(BaseModel):
    project_id: int
    pomo_count: Optional[int] = 0
    price_per_hour: Optional[float] = 0
    total_price: Optional[float] = 0
    collected: Optional[bool] = False


class CardUpdate(BaseModel):
    id: int
    project_id: int
    pomo_count: Optional[int] = 0
    price_per_hour: Optional[float] = 0
    total_price: Optional[float] = 0
    collected: Optional[bool] = False
    created_at: date


class CardResponse(CardCreate):
    id: int
    created_at: date

    class Config:
        orm_mode = True
