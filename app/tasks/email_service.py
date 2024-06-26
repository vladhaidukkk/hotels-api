import smtplib
from email.message import EmailMessage

from app.config import settings


def send_email_message(message: EmailMessage) -> None:
    smtp_server = smtplib.SMTP_SSL if settings.smtp_pass else smtplib.SMTP
    with smtp_server(settings.smtp_host, settings.smtp_port) as server:
        if settings.smtp_pass:
            server.login(settings.smtp_user, settings.smtp_pass)
        server.send_message(message)
