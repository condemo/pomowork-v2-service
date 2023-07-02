from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True
