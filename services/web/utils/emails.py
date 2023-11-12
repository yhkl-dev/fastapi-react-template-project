import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from typing import List

from project.logger import setup_logger

logger = setup_logger()

STMP_USER = "your_smtp_user"
STMP_RECEIVERS = ["receiver1@example.com", "receiver2@example.com"]
SMTP_SERVER = "your_smtp_server"


def send_email(
    subject: str,
    content: str,
    email_receivers: List[str] = STMP_RECEIVERS,
) -> None:
    if not email_receivers:
        logger.error("No email receivers provided")
        return

    receivers = ",".join(email_receivers)
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = STMP_USER
    message["To"] = receivers
    message["Message-id"] = make_msgid()
    message["Date"] = formatdate()
    body = MIMEText(content, "html")
    message.attach(body)

    try:
        with smtplib.SMTP(SMTP_SERVER) as client:
            client.sendmail(STMP_USER, email_receivers, message.as_string())
            logger.info(f"Email delivered successfully!({receivers})")
    except smtplib.SMTPException as e:
        logger.error(f"Email delivery failed: {e}")
        raise e
