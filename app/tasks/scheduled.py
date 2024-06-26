import asyncio
from datetime import UTC, datetime, timedelta

from app.bookings.model import BookingModel
from app.bookings.repo import BookingsRepo
from app.bookings.schemas import Booking
from app.tasks.email_service import send_email_message
from app.tasks.email_templates import create_booking_reminder_message
from app.tasks.worker import worker

# Required for ORM relationships to work.
# isort: split
from app.hotels.model import HotelModel  # noqa
from app.users.model import UserModel  # noqa


async def _send_booking_reminder_email(days: int):
    now = datetime.now(UTC).date() + timedelta(days=days)
    bookings = await BookingsRepo.get_all(BookingModel.date_from == now)
    for booking in bookings:
        booking_dict = Booking.model_validate(booking).model_dump()
        message = create_booking_reminder_message(days=days, booking=booking_dict)
        send_email_message(message)


@worker.task(name="send_booking_reminder_email")
def send_booking_reminder_email(days: int):
    asyncio.run(_send_booking_reminder_email(days=days))
