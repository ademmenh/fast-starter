import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from typing import AsyncGenerator

from src.config.infrastructure.database_adapter import DatabaseAdapter, metadata
from src.config.infrastructure.adapter import ConfigAdapter
from src.auth.infrastructure.password_adapter import PasswordAdapter
from src.app import create_app


@pytest.fixture(scope="session")
def config() -> ConfigAdapter:
    return ConfigAdapter(env_file=".env.test")


@pytest_asyncio.fixture(scope="session")
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


@pytest_asyncio.fixture
async def db_engine(_setup_test_database, config: ConfigAdapter) -> AsyncGenerator[AsyncEngine, None]:
    db = DatabaseAdapter(config)
    engine = db.engine
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    await db.clean_tables()
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def client(_setup_test_database, config: ConfigAdapter, monkeypatch: pytest.MonkeyPatch) -> AsyncGenerator[AsyncClient, None]:
    db = DatabaseAdapter(config)
    async with db.engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    await db.clean_tables()

    async def _mock_hash(self, plain: str) -> str:
        return f"hashed_{plain}"

    async def _mock_compare(self, plain: str, hashed: str) -> bool:
        return hashed == f"hashed_{plain}"

    monkeypatch.setattr(PasswordAdapter, "hash", _mock_hash)
    monkeypatch.setattr(PasswordAdapter, "compare", _mock_compare)

    app = create_app(config=config, show_docs=False)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
