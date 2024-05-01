from datetime import date, datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, Response, status
from pydantic import BaseModel

router = APIRouter(prefix="/bookings", tags=["Bookings"])


class BaseBooking(BaseModel):
    hotel_id: int
    room_id: int
    date_from: date
    date_to: date


class Booking(BaseBooking):
    id: UUID
    created_at: datetime
    updated_at: datetime


class BookingIn(BaseBooking):
    pass


class BookingOut(Booking):
    pass


bookings: list[Booking] = []


@router.post("", status_code=status.HTTP_201_CREATED, response_model=BookingOut)
def create_booking(booking: BookingIn) -> Booking:
    now = datetime.now()
    new_booking = Booking(
        **booking.model_dump(), id=uuid4(), created_at=now, updated_at=now
    )
    bookings.append(new_booking)
    return new_booking


def find_booking_index_by_id(booking_id: UUID) -> int | None:
    return next((i for i, b in enumerate(bookings) if b.id == booking_id), None)


@router.put("/{booking_id}", response_model=BookingOut)
def update_booking(booking_id: UUID, booking: BookingIn, response: Response) -> Booking:
    now = datetime.now()
    existing_idx = find_booking_index_by_id(booking_id)

    if existing_idx is None:
        new_booking = Booking(
            **booking.model_dump(), id=booking_id, created_at=now, updated_at=now
        )
        bookings.append(new_booking)
        response.status_code = status.HTTP_201_CREATED
        return new_booking

    updated_booking = Booking.parse_obj(
        {
            **bookings[existing_idx].model_dump(),
            **booking.model_dump(),
            "updated_at": now,
        }
    )
    bookings[existing_idx] = updated_booking
    return updated_booking
