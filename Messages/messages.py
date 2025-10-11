import os
import smtplib
from email.message import EmailMessage
import ssl

from AlpacaAPI.api import get_cash
from Config.config import EMAILUSER, STARTVALUE
from FastAPI.api import get_all_trades, get_trades_in_range
from Logic.timelogic import get_today_timestamp_range

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


def send_warning(position):
    subject = "Warning: Stock Price Drop Alert"
    body = ("Your stock" + str(position) + "has reached the knockout point, please have a look at it and take some actions if necessary. \n"
            "This is an automated message, please do not reply. Any reply won`t be read or answered.")
    send_email(subject, body)


def send_dayly_report():
    numberoftrades = sum(get_trades_in_range(get_today_timestamp_range()))
    cash = get_cash()
    moneymade = cash - STARTVALUE
    subject = "Daily Report"
    body = ("This is you daily report. \n"
            "This is an automated message, please do not reply. Any reply won`t be read or answered. \n"
            "Today you made " + str(numberoftrades) + " trades. \n"
            "You made a total of " + str(moneymade) + " $ today. \n"
            "Your total balance is after today" + str(cash) + "\n"                                  
            "For further information please check your dashboard.")
    send_email(subject, body)
