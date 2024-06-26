from celery import Celery
from celery.schedules import crontab

from app.config import settings

worker = Celery(
    "tasks",
    broker=settings.redis_url,
    include=["app.tasks.tasks", "app.tasks.scheduled"],
)

worker.conf.beat_schedule = {
    "booking_reminder_1_day": {
        "task": "send_booking_reminder_email",
        "schedule": crontab(hour="9", minute="0"),
        "args": (1,),
    },
    "booking_reminder_3_days": {
        "task": "send_booking_reminder_email",
        "schedule": crontab(hour="15", minute="30"),
        "args": (3,),
    },
}

worker.conf.broker_connection_retry_on_startup = True
