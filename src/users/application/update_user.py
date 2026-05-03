from dataclasses import dataclass, replace
from src.auth.domain.ports import IPasswordAdapter
from src.shared.domain.email import Email
from src.shared.domain.phone import Phone
from src.users.domain.entity import UserEntity, UserRole
from src.users.domain.errors import UserEmailAlreadyExistsError, UserNotFoundError
from src.users.domain.ports import IUserRepository
from typing import Any

@dataclass
class UpdateUserInput:
    user_id: str
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    password: str | None = None
    role: UserRole | None = None


class UpdateUser:
    def __init__(
        self,
        user_repository: IUserRepository,
        password_adapter: IPasswordAdapter,
    ) -> None:
        self._user_repository = user_repository
        self._password_adapter = password_adapter

    async def execute(self, input: UpdateUserInput) -> UserEntity:
        user = await self._user_repository.find_by_id(input.user_id)
        if user is None:
            raise UserNotFoundError(input.user_id)

        updates: dict[str, Any] = {}

        if input.name is not None:
            updates["name"] = input.name.strip()

        if input.email is not None:
            email = Email.create(input.email)
            existing = await self._user_repository.find_by_email(email.value)
            if existing is not None and existing.id.value != input.user_id:
                raise UserEmailAlreadyExistsError(email.value)
            updates["email"] = email

        if input.phone is not None:
            if input.phone is None:
                updates["phone"] = None
            else:
                updates["phone"] = Phone.create(str(input.phone))

        if input.password is not None:
            updates["password_hash"] = await self._password_adapter.hash(input.password)

        if input.role is not None:
            updates["role"] = input.role

        if updates:
            user = replace(user, **updates)

        return await self._user_repository.update(user)
