import configparser
import smtplib
import ssl
import os
from email.message import EmailMessage

PORT = 465
config = configparser.ConfigParser()
config.read('configs/email.ini')


def send_email(subject, message):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
        msg = EmailMessage()
        msg.set_content(message)
        msg["Subject"] = subject
        msg["From"] = config["sender"]["email"]
        msg["To"] = config["receiver"]["email"]
        password = os.environ['EMAIL_PASS']
        server.login(config["sender"]["email"], password)
        server.send_message(msg)
