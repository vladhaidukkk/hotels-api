from sqlalchemy import JSON, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.core import Base
from app.db.mixins import ReprMixin
from app.db.types import IntPrimaryKey


class RoomModel(ReprMixin, Base):
    __tablename__ = "rooms"

    id: Mapped[IntPrimaryKey]
    name: Mapped[str]
    description: Mapped[str | None]
    capacity: Mapped[int]
    services: Mapped[list[str]] = mapped_column(JSON)
    price: Mapped[int]
    quantity: Mapped[int]
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))

    __table_args__ = (
        CheckConstraint("capacity >= 1", name="rooms_capacity_positive_check"),
        CheckConstraint("price >= 1", name="rooms_price_positive_check"),
        CheckConstraint("quantity >= 0", name="rooms_quantity_non_negative_check"),
    )
