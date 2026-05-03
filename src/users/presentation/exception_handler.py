from fastapi import HTTPException
from src.users.domain.errors import UserEmailAlreadyExistsError, UserNotFoundError


class UsersExceptionHandler:
    def __call__(self, exc: Exception) -> None:
        match exc:
            case UserNotFoundError():
                raise HTTPException(
                    status_code=404,
                    detail=getattr(exc, "message", str(exc)),
                )
            case UserEmailAlreadyExistsError():
                raise HTTPException(
                    status_code=409,
                    detail=getattr(exc, "message", str(exc)),
                )
            case _:
                raise exc
