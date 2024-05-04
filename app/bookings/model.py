from datetime import date

from sqlalchemy import CheckConstraint, Computed, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.core import Base
from app.db.mixins import ReprMixin
from app.db.types import CreatedAt, IntPrimaryKey, UpdatedAt


class BookingModel(ReprMixin, Base):
    __tablename__ = "bookings"

    id: Mapped[IntPrimaryKey]
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]
    total_days: Mapped[int] = mapped_column(Computed("date_to - date_from"))
    total_cost: Mapped[int] = mapped_column(Computed("(date_to - date_from) * price"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    __table_args__ = (
        CheckConstraint("price >= 1", name="bookings_price_positive_check"),
        CheckConstraint("date_from < date_to", name="bookings_date_range_check"),
    )
