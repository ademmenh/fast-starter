from sqlalchemy import MetaData, text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from src.config.domain.interface import IConfig

metadata = MetaData()


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

    async def clean_tables(self) -> None:
        async with self._engine.begin() as conn:
            for table in reversed(metadata.sorted_tables):
                await conn.execute(text(f'TRUNCATE TABLE "{table.name}" CASCADE'))
