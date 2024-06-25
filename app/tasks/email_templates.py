from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def _generate_email_message(
    receiver: str, subject: str, html_content: str
) -> EmailMessage:
    message = EmailMessage()
    message["From"] = settings.smtp_user
    message["To"] = settings.smtp_receiver or receiver
    message["Subject"] = subject
    message.set_content(html_content, subtype="html")
    return message


def create_booking_confirmation_message(
    receiver: EmailStr, booking: dict
) -> EmailMessage:
    return _generate_email_message(
        receiver=receiver,
        subject="Booking Confirmation",
        html_content=(
            f"""
            <h1>Booking Confirmation</h1>
            <p>You have booked a hotel from {booking["date_from"]} to {booking["date_to"]}.</p>
            <p>If you did not make this booking, please contact us.</p>
            """
        ),
    )
