import pytest
from src.users.application.get_user import GetUser, GetUserInput
from src.users.domain.entity import UserEntity
from src.shared.domain.id import Id
from src.shared.domain.email import Email
from src.users.infrastructure.repository import InMemoryUserRepository

@pytest.mark.asyncio
async def test_get_user_use_case():
    repo = InMemoryUserRepository()
    import uuid
    user_id = Id(str(uuid.uuid4()))
    entity = UserEntity(
        id=user_id,
        name="Unit Test User",
        email=Email("unit@example.com"),
        phone=None,
        password_hash="hash",
        role="client"
    )
    await repo.create(entity)
    
    use_case = GetUser(repo)
    result = await use_case.execute(GetUserInput(user_id=user_id.value))
    assert result.name == "Unit Test User"
