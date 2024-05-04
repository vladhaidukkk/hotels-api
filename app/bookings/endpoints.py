from datetime import date, datetime

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.bookings.model import BookingModel
from app.db.core import session_factory
from app.rooms.model import RoomModel

router = APIRouter(prefix="/bookings", tags=["Bookings"])


class BookingBase(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date


class BookingIn(BookingBase):
    pass


class BookingOut(BookingBase):
    id: int
    price: int
    total_days: int
    total_cost: int
    created_at: datetime
    updated_at: datetime


@router.post("", status_code=status.HTTP_201_CREATED, response_model=BookingOut)
async def create_booking(data: BookingIn):
    async with session_factory() as session:
        room = await session.get(RoomModel, data.room_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room with this id doesn't exist",
            )

        booking = BookingModel(**data.model_dump(), price=room.price)
        session.add(booking)
        await session.commit()

    return booking
