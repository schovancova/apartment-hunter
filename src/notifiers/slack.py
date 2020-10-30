"""Apartment phone and desktop"""
import os

import configparser
from notifiers.providers.slack import Slack

from src.utils.constants import NOTIFICATIONS_CONFIG_PATH

slack = Slack()

config = configparser.ConfigParser()
config.read(NOTIFICATIONS_CONFIG_PATH)


def send_slack_message(title, url):
    """Send slack message"""
    if config["slack"]["enable_slack"] == "false":
        return
    webhook = os.environ["SLACK_WEBHOOK"]
    slack.notify(message=f"{title} {url}", webhook_url=webhook)