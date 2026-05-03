from pydantic import BaseModel, EmailStr


# // examples
class LoginDto(BaseModel):
    """Example for login"""
    email: EmailStr = "user@gmail.com"
    password: str = "password123"


class RegisterDto(BaseModel):
    """Example for register"""
    name: str = "John Doe"
    email: EmailStr = "user@gmail.com"
    password: str = "password"
    phone: str | None = "123456789"


class RefreshDto(BaseModel):
    """Example for refresh"""
    refresh_token: str = "refresh_token"
