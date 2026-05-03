from datetime import datetime
from src.shared.presentation.responses import CamelModel
from src.users.domain.entity import UserEntity


class UserRDTO(CamelModel):
    id: str
    name: str
    email: str
    phone: str | None
    role: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: UserEntity) -> "UserRDTO":
        return cls(
            id=entity.id.value,
            name=entity.name,
            email=entity.email.value,
            phone=entity.phone.value if entity.phone is not None else None,
            role=entity.role,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
