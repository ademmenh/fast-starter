from dataclasses import dataclass
from src.users.domain.entity import UserEntity, UserRole
from src.users.domain.ports import IUserRepository, ListUsersFilter


@dataclass
class ListUsersInput:
    role: UserRole | None = None
    search: str | None = None
    page: int = 1
    limit: int = 20


class ListUsers:
    def __init__(self, user_repository: IUserRepository) -> None:
        self._user_repository = user_repository

    async def execute(self, input: ListUsersInput) -> tuple[list[UserEntity], int]:
        filter = (
            ListUsersFilter(role=input.role, search=input.search)
            if (input.role or input.search)
            else None
        )
        return await self._user_repository.list(filter, page=input.page, limit=input.limit)
