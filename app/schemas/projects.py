from pydantic import BaseModel
from typing import Optional

from app.schemas.cards import CardResponse


class ProjectBase(BaseModel):
    name: str
    salary_collected: Optional[float] = None
    pending_salary: Optional[float] = None
    total_money: Optional[float] = None
    price_per_hour: Optional[float] = None


class ProjectCreate(ProjectBase):
    owner_id: int


class ProjectUpdate(ProjectBase):
    id: int


class ProjectResponse(ProjectBase):
    id: int
    cards: list[CardResponse]

    class Config:
        orm_mode = True
