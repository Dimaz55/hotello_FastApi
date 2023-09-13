from fastapi import APIRouter, Depends, Response
from starlette.responses import JSONResponse

from app.exceptions import IncorrectCredentialsException, UserExistsException
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dependencies import get_current_user
from app.users.models import User
from app.users.openapi_schemas import openapi_user_register, openapi_user_login, openapi_user_logout, \
    openapi_user_profile
from app.users.repo import UserRepo
from app.users.schemas import UserRegisterSchema, UserResponseSchema

router = APIRouter(prefix="/auth", tags=["Пользователи"])


@router.post("/register", **openapi_user_register)
async def register_user(user_data: UserRegisterSchema):
    """
    Регистрирует нового пользователя
    """
    existing_user = await UserRepo.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserRepo.add(email=user_data.email, hashed_password=hashed_password)
    return JSONResponse({"detail": "User registered succesfully"}, 201)


@router.post("/login", **openapi_user_login)
async def login_user(response: Response, user_data: UserRegisterSchema):
    """
    Аутентифицирует пользователя и добавляет токен пользователя в cookie
    """
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectCredentialsException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"detail": "authenticated succesfully"}


@router.post("/logout", **openapi_user_logout)
async def logout_user(response: Response):
    """
    Удаляет токен пользователя из cookies
    """
    response.delete_cookie("booking_access_token")
    return {"detail": "user logged out succesfully"}


@router.get("/profile", **openapi_user_profile)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Возвращает данные аутентифицированного пользователя
    """
    return current_user
