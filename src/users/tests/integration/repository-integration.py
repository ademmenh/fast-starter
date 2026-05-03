import pytest
import uuid
from dataclasses import replace
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text

from src.users.domain.entity import UserEntity
from src.users.infrastructure.repository import UserRepository
from src.shared.domain.id import Id
from src.shared.domain.email import Email
from src.users.domain.ports import ListUsersFilter

@pytest.fixture(autouse=True)
async def clear_users_table(db_engine: AsyncEngine):
    """Clear users table before each test."""
    async with db_engine.begin() as conn:
        await conn.execute(text("DELETE FROM users"))

@pytest.mark.asyncio
async def test_user_repository_create_and_find(db_engine: AsyncEngine):
    repo = UserRepository(db_engine)
    # Create entity
    user_id = Id(str(uuid.uuid4()))
    email = Email("testrepo@example.com")
    entity = UserEntity(
        id=user_id,
        name="Test Repo User",
        email=email,
        phone=None,
        password_hash="hash",
        role="client"
    )
    
    created = await repo.create(entity)
    assert created.id.value == user_id.value
    assert created.email.value == "testrepo@example.com"
    
    found = await repo.find_by_id(user_id.value)
    assert found is not None
    assert found.name == "Test Repo User"

    found_by_email = await repo.find_by_email("testrepo@example.com")
    assert found_by_email is not None
    assert found_by_email.id.value == user_id.value

@pytest.mark.asyncio
async def test_user_repository_update(db_engine: AsyncEngine):
    repo = UserRepository(db_engine)
    user_id = Id(str(uuid.uuid4()))
    email = Email("update_test@example.com")
    
    entity = UserEntity(
        id=user_id,
        name="Original Name",
        email=email,
        phone=None,
        password_hash="hash",
        role="client"
    )
    await repo.create(entity)
    
    # Update entity
    updated_entity = replace(entity, name="Updated Name", email=Email("new_email@example.com"))
    result = await repo.update(updated_entity)
    
    assert result.name == "Updated Name"
    assert result.email.value == "new_email@example.com"
    
    # Verify via DB fetch
    fetched = await repo.find_by_id(user_id.value)
    assert fetched is not None
    assert fetched.name == "Updated Name"
    assert fetched.email.value == "new_email@example.com"

@pytest.mark.asyncio
async def test_user_repository_delete(db_engine: AsyncEngine):
    repo = UserRepository(db_engine)
    user_id = Id(str(uuid.uuid4()))
    entity = UserEntity(
        id=user_id,
        name="Delete Me",
        email=Email("delete@example.com"),
        phone=None,
        password_hash="hash",
        role="client"
    )
    await repo.create(entity)
    
    # Ensure it's there
    assert await repo.find_by_id(user_id.value) is not None
    
    # Delete it
    await repo.delete(user_id.value)
    
    # Verify it's gone
    assert await repo.find_by_id(user_id.value) is None

@pytest.mark.asyncio
async def test_user_repository_list(db_engine: AsyncEngine):
    repo = UserRepository(db_engine)
    
    users = [
        UserEntity(
            id=Id(str(uuid.uuid4())),
            name="Admin User",
            email=Email("admin1@example.com"),
            phone=None,
            password_hash="hash",
            role="admin"
        ),
        UserEntity(
            id=Id(str(uuid.uuid4())),
            name="Client User A",
            email=Email("client.a@example.com"),
            phone=None,
            password_hash="hash",
            role="client"
        ),
        UserEntity(
            id=Id(str(uuid.uuid4())),
            name="Client User B",
            email=Email("client.b@example.com"),
            phone=None,
            password_hash="hash",
            role="client"
        )
    ]
    
    for u in users:
        await repo.create(u)
        
    # Test list all
    all_users, total = await repo.list()
    assert total == 3
    assert len(all_users) == 3
    
    # Test list with role filter
    admin_users, total_admins = await repo.list(filter=ListUsersFilter(role="admin"))
    assert total_admins == 1
    assert len(admin_users) == 1
    assert admin_users[0].name == "Admin User"
    
    client_users, total_clients = await repo.list(filter=ListUsersFilter(role="client"))
    assert total_clients == 2
    assert len(client_users) == 2
    
    # Test list with search filter
    search_users, total_search = await repo.list(filter=ListUsersFilter(search="Client User A"))
    assert total_search == 1
    assert len(search_users) == 1
    assert search_users[0].email.value == "client.a@example.com"
