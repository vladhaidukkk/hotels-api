from typing import Sequence, Type

from sqlalchemy import select

from app.db.core import Base, session_factory


class BaseRepo[T: Base]:
    @classmethod
    def model(cls) -> Type[T]:
        return cls.__orig_bases__[0].__args__[0]  # type: ignore

    @classmethod
    async def get_all(cls) -> Sequence[T]:
        async with session_factory() as session:
            query = select(cls.model())
            result = await session.execute(query)
            return result.scalars().all()
