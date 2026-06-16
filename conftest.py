import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from src.config.infrastructure.database_adapter import metadata
from src.users.infrastructure.schema import users_table  # Ensure tables are registered
from src.app import create_app
from src.config.infrastructure.adapter import ConfigAdapter, Settings


class TestConfig(ConfigAdapter):
    def __init__(self):
        self._settings = Settings(_env_file=".env.test")

    @property
    def env(self) -> str:
        return "test"


test_config = TestConfig()


@pytest_asyncio.fixture(scope="session")
async def create_test_tables():
    """Create tables once per session."""
    engine = create_async_engine(test_config.async_database_url)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_engine(create_test_tables) -> AsyncEngine:
    """Fresh engine for direct DB operations inside tests."""
    engine = create_async_engine(test_config.async_database_url)
    yield engine
    await engine.dispose()


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
