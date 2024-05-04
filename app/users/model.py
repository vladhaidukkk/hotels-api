from sqlalchemy.orm import Mapped, mapped_column

from app.db.core import Base
from app.db.mixins import ReprMixin
from app.db.types import CreatedAt, IntPrimaryKey, UpdatedAt


class UserModel(ReprMixin, Base):
    __tablename__ = "users"

    id: Mapped[IntPrimaryKey]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    __repr_ignore__ = ["hashed_password"]
