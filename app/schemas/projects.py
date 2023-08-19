from pydantic import BaseModel
from typing import Optional

from app.schemas.cards import CardResponse


class ProjectBase(BaseModel):
    name: str
    salary_collected: Optional[float] = 0
    pending_salary: Optional[float] = 0
    total_money: Optional[float] = 0
    price_per_hour: Optional[float] = 0


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    id: int


class ProjectResponse(ProjectBase):
    id: int
    cards: list[CardResponse]

    class Config:
        orm_mode = True
