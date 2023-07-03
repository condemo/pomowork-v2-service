from app.dependencies.database import get_db
from app.schemas.users import UserCreate, UserResponse
from app.utils.users import password_hash
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.models.users import UserModel


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pass = password_hash(user.password)
    user.password = hashed_pass

    new_user = UserModel(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
