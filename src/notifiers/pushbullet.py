"""Apartment phone and desktop"""
import os

import configparser
from notifiers.providers.pushbullet import Pushbullet

from src.utils.constants import NOTIFICATIONS_CONFIG_PATH

pushbullet = Pushbullet()

config = configparser.ConfigParser()
config.read(NOTIFICATIONS_CONFIG_PATH)


def send_push_message(title, message, url):
    """Send push message"""
    if config["pushbullet"]["enable_push"] == "false":
        return
    token = os.environ["PUSHBULLET_TOKEN"]
    devices = pushbullet.devices(token=token)
    sender = devices[0]['iden']
    for device in devices:
        pushbullet.notify(
            message=message,
            token=token,
            title=title,
            type_='note',
            url=url,
            source_device_iden=sender,
            device_iden=device['iden'])