from app.exceptions import (
    IncorrectCredentialsException,
    UserExistsException,
    NoTokenException,
    WrongTokenException,
    TokenExpiredException
)
from app.hotels.openapi_schemas import openapi_example_factory
from app.users.schemas import UserResponseSchema
from app.utils import DetailResponseSchema

auth_error_responses = openapi_example_factory(
    status_code=401,
    description="Ошибка: пользователь не аутентифицирован",
    examples=[
        ("Токен не найден", NoTokenException.detail),
        ("Неверный формат токена", WrongTokenException.detail),
        ("Токен просрочен", TokenExpiredException.detail)
    ]
)

user_create_success_response = openapi_example_factory(
    status_code=201,
    description="Успешная регистрация",
    examples=[("Успешная регистрация", "User registered succesfully")]
)

user_exists_response = openapi_example_factory(
    status_code=409,
    description="Пользователь c таким email уже существует",
    examples=[("Пользователь уже существует", UserExistsException.detail)]
)

openapi_user_register = {
    "operation_id": "user_create",
    "summary": "Регистрация пользователя",
    "status_code": 201,
    "response_description": "Успешная регистрация",
    "responses": user_create_success_response | user_exists_response
}

user_login_success_response = openapi_example_factory(
    status_code=200,
    description="Успешный вход",
    examples=[("Успешный вход", "user authenticated succesfully")]
)

incorrect_credentials_response = openapi_example_factory(
    status_code=401,
    description="Неверный логин или пароль",
    examples=[
        ("Неверный логин или пароль", IncorrectCredentialsException.detail),
    ]
)

openapi_user_login = {
    "operation_id": "user_login",
    "response_model": DetailResponseSchema,
    "summary": "Аутентификация пользователя",
    "responses": user_login_success_response | incorrect_credentials_response
}

user_logout_response = openapi_example_factory(
    status_code=200,
    description="Успешный выход",
    examples=[("Успешный выход", "user logged out succesfully")]
)

openapi_user_logout = {
    "operation_id": "user_logout",
    "response_model": DetailResponseSchema,
    "summary": "Выход из системы",
    "responses": user_logout_response
}

openapi_user_profile = {
    "operation_id": "user_profile",
    "response_model": UserResponseSchema,
    "summary": "Профиль пользователя",
    "response_description": "Успешный ответ",
    "responses": auth_error_responses
}