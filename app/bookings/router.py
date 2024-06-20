from fastapi import APIRouter, HTTPException, status

from app.bookings.model import BookingModel
from app.bookings.repo import BookingsRepo
from app.bookings.schemas import BookingIn, BookingOut
from app.db.core import session_factory
from app.rooms.model import RoomModel

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("", response_model=list[BookingOut])
async def get_bookings():
    return await BookingsRepo.get_all()


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
