from email.message import EmailMessage

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


def create_booking_confirmation_message(booking: dict) -> EmailMessage:
    return _generate_email_message(
        receiver=booking["user"]["email"],
        subject="Booking confirmation",
        html_content=(
            f"""
            <h1>Booking confirmation</h1>
            <p>You have booked a hotel from {booking["date_from"]} to {booking["date_to"]}.</p>
            <p>If you did not make this booking, please contact us.</p>
            """
        ),
    )


def create_booking_reminder_message(days: int, booking: dict) -> EmailMessage:
    days_str = f"{days} day" if days == 1 else f"{days} days"
    return _generate_email_message(
        receiver=booking["user"]["email"],
        subject=f"{days_str} left until check-in",
        html_content=(
            f"""
            <h1>Booking reminder</h1>
            <p>You have a hotel booking from {booking["date_from"]} to {booking["date_to"]}.</p>
            """
        ),
    )
