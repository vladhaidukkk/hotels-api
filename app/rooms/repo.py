from typing import Sequence

from sqlalchemy import ColumnExpressionArgument, func, select, or_, and_
from sqlalchemy.orm import aliased
from datetime import date

from app.bookings.model import BookingModel
from app.db.core import session_factory
from app.db.repo_base import RepoBase
from app.rooms.model import RoomModel


class RoomsRepo(RepoBase[RoomModel]):
    @classmethod
    async def get_all_with_rooms_left(
        cls,
        *filters: ColumnExpressionArgument[bool],
        date_from: date,
        date_to: date,
    ) -> Sequence[dict]:
        """Query to get rooms with number of their available reservations.

        WITH room_bookings AS (
            SELECT * FROM bookings
            WHERE (date_from <= '2024-05-05' AND '2024-05-05' <= date_to) OR
                  (date_from <= '2024-05-06' AND '2024-05-06' <= date_to)
        )
        SELECT rooms.*, rooms.quantity - COUNT(room_bookings.id) AS rooms_left
        FROM rooms LEFT JOIN room_bookings ON rooms.id = room_bookings.room_id
        GROUP BY rooms.id
        HAVING rooms_left > 0;

        """
        async with session_factory() as session:
            room_bookings = (
                select(BookingModel)
                .filter(
                    or_(
                        and_(
                            BookingModel.date_from <= date_from,
                            date_from <= BookingModel.date_to,
                        ),
                        and_(
                            BookingModel.date_from <= date_to,
                            date_to <= BookingModel.date_to,
                        ),
                    ),
                )
                .cte("room_bookings")
            )
            rooms_left = (RoomModel.quantity - func.count(room_bookings.c.id)).label(
                "rooms_left"
            )
            query = (
                select(RoomModel.__table__.columns, rooms_left)
                .join(
                    room_bookings, room_bookings.c.room_id == RoomModel.id, isouter=True
                )
                .filter(*filters)
                .group_by(RoomModel.id)
                .having(rooms_left > 0)
            )
            result = await session.execute(query)
            return result.mappings().all()
