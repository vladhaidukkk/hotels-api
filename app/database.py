import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import DB_URL

engine = create_async_engine(url=DB_URL, echo=True)


async def print_version():
    async with engine.connect() as conn:
        res = await conn.execute(text("SELECT VERSION()"))
        version_row = res.first()
        if version_row:
            version = version_row[0]
            print(version)


asyncio.run(print_version())
