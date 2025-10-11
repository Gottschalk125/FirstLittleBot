import os
import smtplib
from email.message import EmailMessage
import ssl

from Config.config import EMAILUSER

EMAILSENDER = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def send_email(subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAILSENDER
    msg['To'] = EMAILUSER
    msg.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:

            server.login(EMAILSENDER, PASSWORD)
            server.send_message(msg)

        print("Email sent successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")


def send_warning():
    subject = "Warning: Stock Price Drop Alert"
    body = ("Your stock has reached the knockout point, please have a look at it and take some actions if necessary. \n"
            "This is an automated message, please do not reply. Any reply won`t be read or answered.")
    send_email(subject, body)


def send_dayly_report():
    subject = "Daily Report"
    body = ("This is you daily report. \n"
            "This is an automated message, please do not reply. Any reply won`t be read or answered. \n"
            "")
