from typing import Sequence, Type

from sqlalchemy import ColumnExpressionArgument, delete, insert, select

from app.db.core import Base, session_factory


class RepoBase[T: Base]:
    @classmethod
    def model(cls) -> Type[T]:
        return cls.__orig_bases__[0].__args__[0]  # type: ignore

    @classmethod
    async def get_by_id(cls, id_: int) -> T | None:
        async with session_factory() as session:
            query = select(cls.model()).filter_by(id=id_)
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def get_one_or_none(
        cls, *filters: ColumnExpressionArgument[bool]
    ) -> T | None:
        async with session_factory() as session:
            query = select(cls.model()).filter(*filters)
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def get_all(cls, *filters: ColumnExpressionArgument[bool]) -> Sequence[T]:
        async with session_factory() as session:
            query = select(cls.model()).filter(*filters)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data) -> T:
        async with session_factory() as session:
            stmt = insert(cls.model()).values(**data).returning(cls.model())
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @classmethod
    async def delete_by_id(cls, id_: int) -> None:
        async with session_factory() as session:
            stmt = delete(cls.model()).filter_by(id=id_)
            await session.execute(stmt)
            await session.commit()
