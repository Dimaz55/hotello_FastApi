from datetime import datetime
from typing import Union

from fastapi import Depends
from jose import JWTError, jwt
from starlette.requests import Request
from typing_extensions import Never

from app.config import settings
from app.exceptions import (
    IncorrectCredentialsException,
    NoTokenException,
    TokenExpiredException,
    WrongTokenException,
)
from app.users.models import User
from app.users.repo import UserRepo


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise NoTokenException
    return token


async def get_current_user(
    token: str = Depends(get_token)
) -> Union[User, Never]:
    try:
        payload = jwt.decode(
            token, str(settings.SECRET_KEY), str(settings.ENCRYPT_ALGO)
        )
    except JWTError:
        raise WrongTokenException

    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise IncorrectCredentialsException
    user = await UserRepo.find_by_id(int(user_id))
    if not user:
        raise IncorrectCredentialsException
    return user
