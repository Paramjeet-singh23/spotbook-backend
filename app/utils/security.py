from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from app.config import settings
from uuid import UUID
from fastapi import Header
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Authentication")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[UUID] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str, credentials_exception):
    try:
        token_bytes = token.encode("utf-8")
        payload = jwt.decode(
            token_bytes, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        user_id: UUID = payload.get("user_id")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email, user_id=user_id)
    except Exception as e:
        print(e)
        raise credentials_exception
    return token_data


def get_user_id_from_token(Authentication: str = Header(None)):
    token_type, token = Authentication.split()
    payload = jwt.decode(
        token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
    )
    return UUID(payload.get("user_id"))
