from sqlalchemy import String, Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.dependencies.database import Base


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    salary_collected = Column(Float, nullable=True)
    pending_salary = Column(Float, nullable=True)
    total_money = Column(Float, nullable=True)
    price_per_hour = Column(Float, nullable=True)

    cards = relationship("CardModel")
