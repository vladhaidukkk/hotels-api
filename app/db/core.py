from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import ASYNC_DB_URL, SYNC_DB_URL

sync_engine = create_engine(url=SYNC_DB_URL, echo=True)
async_engine = create_async_engine(url=ASYNC_DB_URL, echo=True)

metadata = MetaData()
