from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

extra_engine_kwargs = {}

if settings.env.null_pool or settings.env.mode == "test":
    extra_engine_kwargs["poolclass"] = NullPool

engine = create_async_engine(
    url=settings.app.db.url, echo=settings.env.debug, **extra_engine_kwargs
)
session_factory = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
