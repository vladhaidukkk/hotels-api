from datetime import date

from sqlalchemy import and_, func, insert, or_, select

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

        WITH booked_rooms AS ( SELECT * FROM bookings WHERE room_id = 1 AND
        (date_from <= '2024-05-05' AND '2024-05-05' <= date_to) OR.

                  (date_from <= '2024-05-06' AND '2024-05-06' <= date_to)
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE room_id = 1
        GROUP BY rooms.quantity;

        """
        async with session_factory() as session:
            booked_rooms = (
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
                .cte("booked_rooms")
            )
            rooms_left_query = (
                select(
                    (RoomModel.quantity - func.count(booked_rooms.c.room_id)).label(
                        "rooms_left"
                    )
                )
                .select_from(RoomModel)
                .join(booked_rooms, booked_rooms.c.room_id == RoomModel.id)
                .filter(RoomModel.id == room_id)
                .group_by(RoomModel.quantity)
            )

            rooms_left_result = await session.execute(rooms_left_query)
            rooms_left: int = rooms_left_result.scalar()

            if rooms_left <= 0:
                return None

            room_price_query = select(RoomModel.price).filter_by(id=room_id)
            room_price_result = await session.execute(room_price_query)
            room_price: int = room_price_result.scalar()

            create_booking_stmt = (
                insert(BookingModel)
                .values(
                    user_id=user_id,
                    room_id=room_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=room_price,
                )
                .returning(BookingModel)
            )
            create_booking_result = await session.execute(create_booking_stmt)
            await session.commit()
            return create_booking_result.scalar()
