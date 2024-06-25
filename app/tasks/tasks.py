import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.tasks.celery_app import celery_app
from app.tasks.email_templates import create_booking_confirmation_message


@celery_app.task
def process_image(path: str) -> None:
    img_path = Path(path)
    img = Image.open(img_path)
    for width, height in [(1000, 500), (200, 100)]:
        resized_img = img.resize(size=(width, height))
        resized_img.save(f"app/static/images/resized_{width}_{height}_{img_path.name}")


@celery_app.task
def send_booking_confirmation_email(
    # EmailStr is just a type. Pydantic won't validate it as it's not a FastAPI endpoint.
    receiver: EmailStr,
    booking: dict,
) -> None:
    smtp_server = smtplib.SMTP_SSL if settings.smtp_pass else smtplib.SMTP
    with smtp_server(settings.smtp_host, settings.smtp_port) as server:
        if settings.smtp_pass:
            server.login(settings.smtp_user, settings.smtp_pass)
        message = create_booking_confirmation_message(
            receiver=receiver, booking=booking
        )
        server.send_message(message)
