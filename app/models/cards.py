from app.dependencies.database import Base
from sqlalchemy import Boolean, Date, Integer, Column, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class CardModel(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    pomo_count = Column(Integer, nullable=False)
    price_per_hour = Column(Float, nullable=True)
    total_price = Column(Float, nullable=True)
    collected = Column(Boolean, nullable=False)
    created_at = Column(Date, nullable=False, server_default=func.current_date())

    project = relationship("ProjectModel", back_populates="cards")
