from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.core import Base
from app.db.mixins import ReprMixin
from app.db.types import CreatedAt, IntPrimaryKey, UpdatedAt

if TYPE_CHECKING:
    from app.bookings.model import BookingModel


class UserModel(ReprMixin, Base):
    __tablename__ = "users"

    id: Mapped[IntPrimaryKey]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    bookings: Mapped[list["BookingModel"]] = relationship(back_populates="user")

    __repr_ignore__ = ["hashed_password"]

    def __str__(self) -> str:
        return f"User #{self.id}"
