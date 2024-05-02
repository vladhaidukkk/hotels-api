from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import ASYNC_DB_URL, SYNC_DB_URL

sync_engine = create_engine(url=SYNC_DB_URL, echo=True)
async_engine = create_async_engine(url=ASYNC_DB_URL, echo=True)

sync_session = sessionmaker(sync_engine)
async_session = async_sessionmaker(async_engine)

metadata = MetaData()


class Base(DeclarativeBase):
    pass
