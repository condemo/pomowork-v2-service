from app.dependencies.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Time
from sqlalchemy.orm import relationship


class PomoTimerModel(Base):
    __tablename__ = "pomodoro"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    time = Column(Time, nullable=False)

    project = relationship("ProjectModel", back_populates="pomodoro")
