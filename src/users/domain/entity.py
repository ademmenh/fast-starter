from dataclasses import dataclass, field
from datetime import UTC, datetime
from src.shared.domain.email import Email
from src.shared.domain.id import Id
from src.shared.domain.phone import Phone
from typing import Literal

UserRole = Literal["admin", "client"]


@dataclass(frozen=True)
class UserEntity:
    id: Id
    name: str
    email: Email
    phone: Phone | None
    password_hash: str
    role: UserRole
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def is_admin(self) -> bool:
        return self.role == "admin"

    def is_client(self) -> bool:
        return self.role == "client"

    def can_manage_users(self) -> bool:
        return self.is_admin()

    def can_manage_meals(self) -> bool:
        return self.is_admin()
