from pydantic import BaseModel, EmailStr
from typing import Literal

UserRoleEnum = Literal["admin", "client"]


class RegisterUserDto(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str | None = None


class UpdateUserDto(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    password: str | None = None
