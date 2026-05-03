from fastapi import HTTPException
from src.auth.domain.errors import InvalidCredentialsError, InvalidRefreshTokenError
from src.users.domain.errors import UserEmailAlreadyExistsError

class AuthExceptionHandler:
    def __call__(self, exc: Exception) -> None:
        match exc:
            case InvalidCredentialsError():
                raise HTTPException(
                    status_code=401,
                    detail="Invalid Credentials",
                )
            case InvalidRefreshTokenError():
                raise HTTPException(
                    status_code=401,
                    detail="Invalid Refresh Token",
                )
            case UserEmailAlreadyExistsError():
                raise HTTPException(
                    status_code=409,
                    detail="User email already exists",
                )
            case _:
                raise exc
