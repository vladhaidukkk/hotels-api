import smtplib
from email.message import EmailMessage

from app.config import settings


def send_email_message(message: EmailMessage) -> None:
    smtp_server = smtplib.SMTP_SSL if settings.app.smtp.password else smtplib.SMTP
    with smtp_server(settings.app.smtp.host, settings.app.smtp.port) as server:
        if settings.app.smtp.password:
            server.login(settings.app.smtp.user, settings.app.smtp.password)
        server.send_message(message)
