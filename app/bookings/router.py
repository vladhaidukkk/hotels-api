from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.bookings.model import BookingModel
from app.bookings.repo import BookingsRepo
from app.bookings.schemas import BookingIn, BookingOut
from app.db.core import session_factory
from app.rooms.model import RoomModel
from app.users.deps import get_current_user
from app.users.model import UserModel

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("", response_model=list[BookingOut])
async def get_bookings(user: Annotated[UserModel, Depends(get_current_user)]):
    return await BookingsRepo.get_all(BookingModel.user_id == user.id)


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
