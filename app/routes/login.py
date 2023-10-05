from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.oauth2 import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token
)
from app.models.users import UserModel
from app.utils.users import password_verify


router = APIRouter(
    prefix="/login",
    tags=["Authentication"],
)


@router.post("/")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials",
        )

    if not password_verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials",
        )

    access_token = create_access_token(data={"user_id": user.id})
    refresh_token = create_refresh_token(data={"username": user.username})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
async def refresh_token(new_token: str = Depends(verify_refresh_token)):
    return {
        "access_token": new_token,
        "token_type": "bearer"
    }
