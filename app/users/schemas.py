from pydantic import BaseModel, EmailStr


class UserResponseSchema(BaseModel):
    email: EmailStr
    

class UserRegisterSchema(UserResponseSchema):
    password: str
