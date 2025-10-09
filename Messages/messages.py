import smtplib
import sys
import os
from dotenv import load_dotenv

from Config.config import Phone_number

Carriers = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}
load_dotenv()
Email = os.getenv("EMAIL")
Password = os.getenv("PASSWORD")

def send_message(carrier, message):
    phone_number = Phone_number
    recipient = phone_number + Carriers[carrier]
    auth = (Email, Password)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    server.sendmail(auth[0], recipient, message)


# Delete lateron, not needed for my usage
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(f"Usage: python3 {sys.argv[0]} <PHONE_NUMBER> <CARRIER> <MESSAGE>")
        sys.exit(0)

    phone_number = sys.argv[1]
    carrier = sys.argv[2]
    message = sys.argv[3]

    send_message(carrier, message)

