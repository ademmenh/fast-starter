import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
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


@pytest.fixture(autouse=True, scope="session")
async def _setup_test_database(config: ConfigAdapter):
    db_name = config.db_name
    maintenance_url = config.async_database_url.rsplit("/", 1)[0] + "/postgres"
    engine = create_async_engine(maintenance_url, isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        await conn.execute(text(f'DROP DATABASE IF EXISTS "{db_name}"'))
        await conn.execute(text(f'CREATE DATABASE "{db_name}"'))
    await engine.dispose()
    yield
    engine = create_async_engine(maintenance_url, isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        await conn.execute(
            text(f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{db_name}'
                  AND pid <> pg_backend_pid()
            """)
        )
        await conn.execute(text(f'DROP DATABASE IF EXISTS "{db_name}"'))
    await engine.dispose()


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
