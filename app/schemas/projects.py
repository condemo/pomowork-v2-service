from pydantic import BaseModel
from typing import Optional

from app.schemas.cards import CardResponse
from app.schemas.pomodoros import PomodoroResponse


class ProjectCreate(BaseModel):
    name: str
    salary_collected: Optional[float] = None
    pending_salary: Optional[float] = None
    total_money: Optional[float] = None
    price_per_hour: Optional[float] = None


class ProjectUpdate(ProjectCreate):
    pass


class ProjectResponse(ProjectCreate):
    id: int
    cards: list[CardResponse]
    pomodoro: PomodoroResponse

    class Config:
        orm_mode = True
