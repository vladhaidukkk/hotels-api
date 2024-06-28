import pytest
from sqlalchemy import delete

from app.config import mode
from app.db.core import Base, engine

# isort: split
from app.bookings.model import BookingModel  # noqa
from app.hotels.model import HotelModel  # noqa
from app.rooms.model import RoomModel  # noqa
from app.users.model import UserModel  # noqa

assert mode == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(autouse=True)
async def clear_db_records(request):
    yield

    db_marker = request.node.get_closest_marker("db")
    if not db_marker:
        return

    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(delete(table))
