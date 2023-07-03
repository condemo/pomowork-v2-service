from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql import func
from app.dependencies.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(Date, nullable=False, server_default=func.current_date())
