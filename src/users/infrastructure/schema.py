from sqlalchemy import Column, DateTime, String, Table, func
from sqlalchemy.dialects.postgresql import UUID

from src.shared.infrastructure.metadata import metadata

users_table = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=False), primary_key=True),
    Column("name", String, nullable=False),
    Column("email", String, nullable=False, unique=True, index=True),
    Column("phone", String, nullable=True),
    Column("password_hash", String, nullable=False),
    Column("role", String, nullable=False, default="client"),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
)
