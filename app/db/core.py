from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(url=settings.db_url, echo=True)
session_factory = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass
