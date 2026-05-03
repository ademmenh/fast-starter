from sqlalchemy import Row

from src.shared.domain.email import Email
from src.shared.domain.id import Id
from src.shared.domain.phone import Phone
from src.users.domain.entity import UserEntity


class UserMapper:
    @staticmethod
    def to_domain(row: Row) -> UserEntity:
        return UserEntity(
            id=Id.from_str(row.id),
            name=row.name,
            email=Email.create(row.email),
            phone=Phone.create(row.phone) if row.phone is not None else None,
            password_hash=row.password_hash,
            role=row.role,  # type: ignore[arg-type]
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    @staticmethod
    def to_values(entity: UserEntity) -> dict:
        return {
            "id": entity.id.value,
            "name": entity.name,
            "email": entity.email.value,
            "phone": entity.phone.value if entity.phone is not None else None,
            "password_hash": entity.password_hash,
            "role": entity.role,
        }
