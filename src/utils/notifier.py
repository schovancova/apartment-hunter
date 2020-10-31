"""Notifier class"""
import os
import configparser
from notifiers import get_notifier

import src.utils.constants as const


class Notifier:
    def __init__(self):
        self.enabled = []
        self.email_pass = self.receiver = self.sender = None
        self.push_token = None
        self.slack_webhook = None

        config = configparser.ConfigParser(default_section=None)
        config.read(const.NOTIFICATIONS_CONFIG_PATH)
        self.parse_notification_config(config)

    def parse_notification_config(self, config):
        """Parse notification config"""
        notification_types = list(dict(config.items()).keys())[1:]
        for notification in notification_types:
            if notification == const.EMAIL_NOTIFY:
                self.email_pass = self.get_env_variable("EMAIL_PASS", notification)
                try:
                    self.sender = config[const.EMAIL_NOTIFY]["sender"]
                    self.receiver = config[const.EMAIL_NOTIFY]["receiver"]
                except KeyError:
                    exit(f"{notification} notification if enabled, but sender/receiver"
                         f" is missing in notification config")
            elif notification == const.PUSH_NOTIFY:
                self.push_token = self.get_env_variable("PUSHBULLET_TOKEN", notification)
            elif notification == const.SLACK_NOTIFY:
                self.slack_webhook = self.get_env_variable("SLACK_WEBHOOK", notification)
            self.enabled.append(notification)

    @staticmethod
    def get_env_variable(var_nme, notification):
        if var_nme in os.environ:
            return os.environ[var_nme]
        else:
            exit(f"{notification} notification is enabled, but"
                 f"{var_nme} is missing in env variables")

    def notify_all(self, subject, message, url):
        if const.EMAIL_NOTIFY in self.enabled:
            self.send_email(subject, message)
        if const.SLACK_NOTIFY in self.enabled:
            self.send_slack_message(subject, url)
        if const.PUSH_NOTIFY in self.enabled:
            self.send_push_message(subject, message, url)

    def send_email(self, subject, message):
        """Send email"""
        gmail = get_notifier("gmail")
        gmail.notify(subject=subject, to=self.receiver, message=message,
                     username=self.sender, password=self.email_pass)

    def send_push_message(self, subject, message, url):
        """Send push message"""
        pushbullet = get_notifier("pushbullet")
        devices = pushbullet.devices(token=self.push_token)
        sender = devices[0]['iden']
        for device in devices:
            pushbullet.notify(
                message=message, token=self.push_token, title=subject, type_='note',
                url=url, source_device_iden=sender, device_iden=device['iden'])

    def send_slack_message(self, subject, url):
        """Send slack message"""
        slack = get_notifier("slack")
        slack.notify(message=f"{subject} {url}", webhook_url=self.slack_webhook)


