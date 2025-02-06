import os
from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url=os.environ["DATABASE_URL"],
        modules={'src.models': ['src.models']}
    )
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()