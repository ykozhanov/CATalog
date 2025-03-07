from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    username: str
    password: str


class RegisterSchema(BaseModel):
    username: str
    password: bytes
    email: EmailStr
