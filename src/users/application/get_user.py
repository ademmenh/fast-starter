from dataclasses import dataclass
from datetime import datetime
from src.users.domain.errors import UserNotFoundError
from src.users.domain.ports import IUserRepository

@dataclass
class GetUserOutput:
    id: str
    name: str
    email: str
    phone: str | None
    role: str
    created_at: datetime
    updated_at: datetime

@dataclass
class GetUserInput:
    user_id: str

class GetUser:
    def __init__(self, user_repository: IUserRepository) -> None:
        self._user_repository = user_repository

    async def execute(self, input: GetUserInput) -> GetUserOutput:
        user = await self._user_repository.find_by_id(input.user_id)
        if user is None:
            raise UserNotFoundError(input.user_id)
        return GetUserOutput(
            id=user.id.value,
            name=user.name,
            email=user.email.value,
            phone=user.phone.value if user.phone else None,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
