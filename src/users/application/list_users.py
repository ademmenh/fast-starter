from dataclasses import dataclass
from datetime import datetime
from src.users.domain.entity import UserEntity, UserRole
from src.users.domain.ports import IUserRepository, ListUsersFilter

@dataclass
class ListUsersItemOutput:
    id: str
    name: str
    email: str
    phone: str | None
    role: str
    created_at: datetime
    updated_at: datetime

@dataclass
class ListUsersInput:
    role: UserRole | None = None
    search: str | None = None
    page: int = 1
    limit: int = 20


class ListUsers:
    def __init__(self, user_repository: IUserRepository) -> None:
        self._user_repository = user_repository

    @staticmethod
    def _to_output(user: UserEntity) -> ListUsersItemOutput:
        return ListUsersItemOutput(
            id=user.id.value,
            name=user.name,
            email=user.email.value,
            phone=user.phone.value if user.phone else None,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def execute(self, input: ListUsersInput) -> tuple[list[ListUsersItemOutput], int]:
        filter = (
            ListUsersFilter(role=input.role, search=input.search)
            if (input.role or input.search)
            else None
        )
        users, total = await self._user_repository.list(filter, page=input.page, limit=input.limit)
        items = [self._to_output(u) for u in users]
        return items, total
