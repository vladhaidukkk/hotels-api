import asyncio
from datetime import UTC, datetime, timedelta

from app.bookings.model import BookingModel
from app.bookings.repo import BookingsRepo
from app.bookings.schemas import BookingOut
from app.tasks.celery_app import celery_app
from app.tasks.email_service import send_email_message
from app.tasks.email_templates import create_booking_reminder_message
from app.users.repo import UsersRepo


async def _send_booking_reminder_email(days: int):
    now = datetime.now(UTC).date() + timedelta(days=days)
    bookings = await BookingsRepo.get_all(BookingModel.date_from == now)
    for booking in bookings:
        # TODO: instead of querying user for each booking, join users to bookings.
        receiver = await UsersRepo.get_by_id(booking.user_id)
        booking_dict = BookingOut.model_validate(booking).model_dump()
        message = create_booking_reminder_message(
            days=days, receiver=receiver.email, booking=booking_dict
        )
        send_email_message(message)


@celery_app.task(name="send_booking_reminder_email")
def send_booking_reminder_email(days: int):
    asyncio.run(_send_booking_reminder_email(days=days))
