from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from starlette import status

from app.config import settings
from app.exceptions import IncorrectCredentialsException
from app.users.repo import UserRepo

pwd_context = CryptContext(schemes=["bcrypt"])


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ENCRYPT_ALGO)
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UserRepo.find_one_or_none(email=email)
    if user and verify_password(password, user.hashed_password):
        return user
    raise IncorrectCredentialsException
