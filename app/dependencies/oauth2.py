from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWSError, ExpiredSignatureError

from datetime import datetime, timedelta

from app.dependencies.database import get_db
from app.config import settings
from app.models.users import UserModel
from app.schemas.tokens import TokenData


oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")
oauth_refresh = OAuth2PasswordBearer(tokenUrl="login/refresh")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_DAYS = settings.access_token_expire_days
REFRESH_TOKEN_DAYS = settings.refresh_token_expire_days

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_DAYS)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_DAYS)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = TokenData(id=id)

    except JWSError:
        raise credentials_exception

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return token_data


def verify_refresh_token(token: int = Depends(oauth_refresh),
                         db: Session = Depends(get_db)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception

    except JWSError:
        raise credentials_exception

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = db.query(UserModel).filter(UserModel.username == username).first()
    new_token = create_access_token(data={"user_id": user.id})

    return new_token


def get_current_user(token: int = Depends(oauth_scheme), db: Session = Depends(get_db)):
    token = verify_access_token(token)

    user = db.query(UserModel).filter(UserModel.id == token.id).first()

    return user
