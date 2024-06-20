from datetime import date

from sqlalchemy import and_, func, or_, select

from app.bookings.model import BookingModel
from app.db.core import session_factory
from app.db.repo_base import RepoBase
from app.rooms.model import RoomModel


class BookingsRepo(RepoBase[BookingModel]):
    @classmethod
    async def add(
        cls, user_id: int, room_id: int, date_from: date, date_to: date
    ) -> BookingModel | None:
        """Query to get the number of available reservations for a specific room.

        WITH room_bookings AS (
            SELECT * FROM bookings
            WHERE room_id = :room_id AND
                  (date_from <= :date_from AND :date_from <= date_to) OR
                  (date_from <= :date_to AND :date_to <= date_to)
        )
        SELECT rooms.quantity - COUNT(room_bookings.room_id) FROM rooms
        LEFT JOIN room_bookings ON room_bookings.room_id = rooms.id
        WHERE room_id = :room_id
        GROUP BY rooms.quantity;

        """
        async with session_factory() as session:
            room_bookings = (
                select(BookingModel)
                .filter(
                    BookingModel.room_id == room_id,
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
            rooms_left_query = (
                select(
                    (RoomModel.quantity - func.count(room_bookings.c.room_id)).label(
                        "rooms_left"
                    )
                )
                .select_from(RoomModel)
                .join(
                    room_bookings, room_bookings.c.room_id == RoomModel.id, isouter=True
                )
                .filter(RoomModel.id == room_id)
                .group_by(RoomModel.quantity)
            )
            rooms_left_result = await session.execute(rooms_left_query)
            rooms_left: int = rooms_left_result.scalar()

            if rooms_left < 1:
                return None

            room_price_query = select(RoomModel.price).filter_by(id=room_id)
            room_price_result = await session.execute(room_price_query)
            room_price: int = room_price_result.scalar()

            return await super().add(
                user_id=user_id,
                room_id=room_id,
                date_from=date_from,
                date_to=date_to,
                price=room_price,
            )
