from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from src.config.domain.interface import IConfig
from src.shared.infrastructure.metadata import metadata

class DatabaseAdapter:
    def __init__(self, config: IConfig) -> None:
        self._engine = create_async_engine(
            config.async_database_url,
            echo=config.debug,
            pool_pre_ping=True,
        )

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    async def create_tables(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(metadata.create_all)
