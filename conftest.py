import pytest
import pytest_asyncio
import os
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from src.shared.infrastructure.metadata import metadata
from src.users.infrastructure.schema import users_table  # Ensure tables are registered
from src.app import create_app
from src.config.infrastructure.adapter import ConfigAdapter

TEST_DB_FILE = "test_db.sqlite"
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{TEST_DB_FILE}"

class TestConfig(ConfigAdapter):
    @property
    def async_database_url(self) -> str:
        return TEST_DATABASE_URL

    @property
    def env(self) -> str:
        return "test"

test_config = TestConfig()

test_engine = create_async_engine(
    test_config.async_database_url,
    connect_args={"check_same_thread": False},
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_test_tables():
    # Ensure fresh DB
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)
        
    async with test_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    
    await test_engine.dispose()
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)


@pytest_asyncio.fixture
async def db_engine():
    """Standalone engine for direct DB operations inside tests."""
    yield test_engine


@pytest_asyncio.fixture
async def client():
    """
    HTTP test client.
    """
    app = create_app(config=test_config, show_docs=False)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
