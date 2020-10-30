"""Apartment notifications"""
import configparser
import smtplib
import ssl
import os
import sys
from email.message import EmailMessage
from src.utils.constants import SMTP_PORT, EMAIL_CONFIG_PATH, SMTP_SERVER


config = configparser.ConfigParser()
config.read(EMAIL_CONFIG_PATH)


def send_email(subject, message):
    """Send email"""
    if config["common"]["enable_email"] == "false":
        return
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        msg = EmailMessage()
        msg.set_content(message)
        msg["Subject"] = subject
        msg["From"] = config["sender"]["email"]
        msg["To"] = config["receiver"]["email"]
        try:
            password = os.environ['EMAIL_PASS']
        except KeyError:
            sys.exit("Please input EMAIL_PASS into environment variables")
        server.login(config["sender"]["email"], password)
        server.send_message(msg)
