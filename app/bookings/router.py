from typing import Sequence

from fastapi import APIRouter, status

from app.bookings.model import BookingModel
from app.bookings.repo import BookingsRepo
from app.bookings.schemas import Booking, BookingIn, BookingOut
from app.db.core import session_factory
from app.exceptions import booking_not_found, room_not_found, unavailable_room
from app.rooms.model import RoomModel
from app.tasks.tasks import send_booking_confirmation_email
from app.users.deps import CurrentUser

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("", response_model=list[BookingOut])
async def get_bookings(user: CurrentUser) -> Sequence[BookingModel]:
    return await BookingsRepo.get_all(BookingModel.user_id == user.id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=BookingOut)
async def create_booking(user: CurrentUser, data: BookingIn) -> BookingModel:
    async with session_factory() as session:
        room = await session.get(RoomModel, data.room_id)
        if not room:
            raise room_not_found

    booking = await BookingsRepo.add(user_id=user.id, **data.model_dump())
    if not booking:
        raise unavailable_room

    # Get it again to have the related user.
    booking = await BookingsRepo.get_by_id(booking.id)
    booking_dict = Booking.model_validate(booking).model_dump()
    send_booking_confirmation_email.delay(booking=booking_dict)

    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(user: CurrentUser, booking_id: int):
    booking = await BookingsRepo.get_by_id(booking_id)
    if not booking or booking.user_id != user.id:
        raise booking_not_found

    await BookingsRepo.delete_by_id(booking_id)
