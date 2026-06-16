from pydantic import BaseModel, EmailStr, Field


class LoginDto(BaseModel):
    email: EmailStr = Field(..., examples=["user@gmail.com"])
    password: str = Field(..., examples=["password123"])


class RegisterDto(BaseModel):
    name: str = Field(..., examples=["John Doe"])
    email: EmailStr = Field(..., examples=["user@gmail.com"])
    password: str = Field(..., examples=["password"])
    phone: str | None = Field(None, examples=["123456789"])


class RefreshDto(BaseModel):
    refresh_token: str = Field(..., examples=["refresh_token"])
