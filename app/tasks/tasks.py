from pathlib import Path

from PIL import Image

from app.tasks.celery_app import celery_app
from app.tasks.email_service import send_email_message
from app.tasks.email_templates import create_booking_confirmation_message


@celery_app.task
def process_image(path: str) -> None:
    img_path = Path(path)
    img = Image.open(img_path)
    for width, height in [(1000, 500), (200, 100)]:
        resized_img = img.resize(size=(width, height))
        resized_img.save(f"app/static/images/resized_{width}_{height}_{img_path.name}")


@celery_app.task
def send_booking_confirmation_email(booking: dict) -> None:
    message = create_booking_confirmation_message(booking=booking)
    send_email_message(message)
