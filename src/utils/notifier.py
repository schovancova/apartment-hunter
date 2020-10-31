"""Notifier class"""
import os
import configparser
from notifiers import get_notifier

import src.utils.constants as const
from src.validation.config_validator import validate_config
from src.validation.definitions import NOTIFICATION_VALIDATORS


class Notifier:
    def __init__(self):
        self.enabled = []
        self.gmail_pass = self.g_receiver = self.g_sender = None
        self.email_pass = self.e_receiver = self.e_sender = self.e_server = self.e_port = None
        self.push_token = None
        self.slack_webhook = None

        config = configparser.ConfigParser(default_section=None)
        config.read(const.NOTIFICATIONS_CONFIG_PATH)
        validate_config(config, NOTIFICATION_VALIDATORS)
        self.parse_notification_config(config)

    def parse_notification_config(self, config):
        """Parse notification config"""
        notification_types = list(dict(config.items()).keys())[1:]
        for notification in notification_types:
            if not config.getboolean(notification, "enabled"):
                continue
            if notification == const.GMAIL_NOTIFY:
                self.gmail_pass = self.get_env_variable("GMAIL_PASS", notification)
                self.g_sender = config[notification]["sender"]
                self.g_receiver = config[notification]["receiver"]
            elif notification == const.EMAIL_NOTIFY:
                self.email_pass = self.get_env_variable("EMAIL_PASS", notification)
                self.e_sender = config[notification]["sender"]
                self.e_receiver = config[notification]["receiver"]
                self.e_port = int(config[notification]["smtp_port"])
                self.e_server = config[notification]["smtp_server"]
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
            exit(f"{notification} notification is enabled, but "
                 f"{var_nme} is missing in env variables")

    def notify_all(self, subject, message, url):
        if const.GMAIL_NOTIFY in self.enabled:
            self.send_gmail(subject, message)
        if const.EMAIL_NOTIFY in self.enabled:
            self.send_email(subject, message)
        if const.SLACK_NOTIFY in self.enabled:
            self.send_slack_message(subject, url)
        if const.PUSH_NOTIFY in self.enabled:
            self.send_push_message(subject, message, url)

    def send_gmail(self, subject, message):
        """Send gmail"""
        gmail = get_notifier("gmail")
        gmail.notify(subject=subject, to=self.g_receiver, message=message,
                     username=self.g_sender, password=self.gmail_pass)

    def send_email(self, subject, message):
        """Send gmail"""
        email = get_notifier("email")
        email.notify(subject=subject, to=self.e_receiver, message=message,
                     username=self.e_sender, password=self.email_pass,
                     host=self.e_server, port=self.e_port, tls=True)

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


