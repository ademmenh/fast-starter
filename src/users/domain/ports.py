from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from src.users.domain.entity import UserEntity, UserRole


@dataclass
class CreateUserRDTO:
    id: str
    name: str
    email: str
    phone: str | None
    password_hash: str
    role: UserRole


@dataclass
class UpdateUserRDTO:
    name: str | None = None
    email: str | None = None
    password_hash: str | None = None
    role: UserRole | None = None
    phone: str | None = None


@dataclass
class ListUsersFilter:
    role: UserRole | None = None
    search: str | None = None


class IUserRepository(ABC):
    @abstractmethod
    async def find_by_id(self, user_id: str) -> UserEntity | None: ...

    @abstractmethod
    async def find_by_email(self, email: str) -> UserEntity | None: ...

    @abstractmethod
    async def list(
        self,
        filter: ListUsersFilter | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[UserEntity], int]: ...

    @abstractmethod
    async def create(self, entity: UserEntity) -> UserEntity: ...

    @abstractmethod
    async def update(self, entity: UserEntity) -> UserEntity: ...

    @abstractmethod
    async def delete(self, user_id: str) -> None: ...
