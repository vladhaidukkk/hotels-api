from typing import Sequence

from sqlalchemy import ColumnExpressionArgument, func, select

from app.bookings.model import BookingModel
from app.db.core import session_factory
from app.db.repo_base import RepoBase
from app.rooms.model import RoomModel


class RoomsRepo(RepoBase[RoomModel]):
    @classmethod
    async def get_all_with_rooms_left(
        cls, *filters: ColumnExpressionArgument[bool]
    ) -> Sequence[dict]:
        """Query to get rooms with number of their available reservations.

        SELECT rooms.*, rooms.quantity - COUNT(bookings.id) AS rooms_left
        FROM rooms LEFT JOIN bookings ON rooms.id = bookings.room_id
        GROUP BY rooms.id;

        """
        async with session_factory() as session:
            query = (
                select(
                    RoomModel.__table__.columns,
                    (RoomModel.quantity - func.count(BookingModel.id)).label(
                        "rooms_left"
                    ),
                )
                .join(BookingModel, BookingModel.room_id == RoomModel.id, isouter=True)
                .filter(*filters)
                .group_by(RoomModel.id)
            )
            result = await session.execute(query)
            return result.mappings().all()
