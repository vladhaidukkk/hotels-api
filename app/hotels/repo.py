from datetime import date
from typing import Sequence

from sqlalchemy import ColumnExpressionArgument, and_, func, or_, select

from app.bookings.model import BookingModel
from app.db.core import session_factory
from app.db.repo_base import RepoBase
from app.hotels.model import HotelModel
from app.rooms.model import RoomModel


class HotelsRepo(RepoBase[HotelModel]):
    @classmethod
    async def get_available_hotels(
        cls, *filters: ColumnExpressionArgument[bool], date_from: date, date_to: date
    ) -> Sequence[dict]:
        """Query to get hotels with available rooms.

        WITH room_bookings AS (
            SELECT * FROM bookings
            WHERE (date_from <= :date_from AND :date_from <= date_to) OR
                  (date_from <= :date_to AND :date_to <= date_to)
        ),
        rooms_with_left AS (
            SELECT rooms.*, rooms.quantity - COUNT(room_bookings.room_id) AS quantity_left
            FROM rooms LEFT JOIN room_bookings ON rooms.id = room_bookings.room_id
            GROUP BY rooms.id
        )
        SELECT hotels.*, SUM(rooms_with_left.quantity) AS rooms_quantity, SUM(rooms_with_left.quantity_left) AS rooms_left
        FROM hotels LEFT JOIN rooms_with_left ON hotels.id = rooms_with_left.hotel_id
        GROUP BY hotels.id
        HAVING SUM(rooms_with_left.quantity_left) > 0;

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
            rooms_with_left = (
                select(
                    RoomModel.__table__.columns,
                    (RoomModel.quantity - func.count(room_bookings.c.room_id)).label(
                        "quantity_left"
                    ),
                )
                .select_from(RoomModel)
                .join(
                    room_bookings, room_bookings.c.room_id == RoomModel.id, isouter=True
                )
                .group_by(RoomModel.id)
                .cte("rooms_with_left")
            )
            rooms_left_col = func.sum(rooms_with_left.c.quantity_left).label(
                "rooms_left"
            )
            query = (
                select(
                    HotelModel.__table__.columns,
                    func.sum(rooms_with_left.c.quantity).label("rooms_quantity"),
                    rooms_left_col,
                )
                .select_from(HotelModel)
                .join(
                    rooms_with_left,
                    rooms_with_left.c.hotel_id == HotelModel.id,
                    isouter=True,
                )
                .filter(*filters)
                .group_by(HotelModel.id)
                .having(rooms_left_col > 0)
            )
            result = await session.execute(query)
            return result.mappings().all()
