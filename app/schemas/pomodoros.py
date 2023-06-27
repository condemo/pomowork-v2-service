from pydantic import BaseModel
from datetime import datetime


class PomodoroUpdate(BaseModel):
    project_id: int
    time: datetime.time


class PomodoroResponse(PomodoroUpdate):
    id: int

    class Config:
        orm_mode = True
