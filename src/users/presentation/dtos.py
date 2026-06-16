from pydantic import BaseModel, EmailStr, Field
from typing import Literal

UserRoleEnum = Literal["admin", "client"]


class RegisterUserDto(BaseModel):
    name: str = Field(..., examples=["John Doe"])
    email: EmailStr = Field(..., examples=["user@gmail.com"])
    password: str = Field(..., examples=["password"])
    phone: str | None = Field(None, examples=["123456789"])


class UpdateUserDto(BaseModel):
    name: str | None = Field(None, examples=["John Doe"])
    email: EmailStr | None = Field(None, examples=["user@gmail.com"])
    phone: str | None = Field(None, examples=["123456789"])
    password: str | None = Field(None, examples=["password"])
