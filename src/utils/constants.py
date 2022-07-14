"""Constants"""
EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"
CONFIG_PATH = 'configs/apartments.ini'
NOTIFICATIONS_CONFIG_PATH = 'configs/notifications.ini'
DB_PATH = 'db/main.db'
SMTP_PORT = 465
SMTP_SERVER = "smtp.gmail.com"
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'}

ULOVDOMOV_NAME = "ulov_domov"
BEZREALITKY_NAME = "bez_realitky"
SREALITY_NAME = "sreality"

GMAIL_NOTIFY = "gmail"
EMAIL_NOTIFY = "email"
PUSH_NOTIFY = "pushbullet"
SLACK_NOTIFY = "slack"

CHECK_FREQUENCY_IN_SECONDS = 180

SREALITY_SITE_TYPES = {
    "1+kk": 2,
    "1+1": 3,
    "2+kk": 4,
    "2+1": 5,
    "3+kk": 6,
    "3+1": 7,
    "4+kk": 8,
    "4+1": 9,
    "5+1": 11,
    "5+kk": 10,
    "room": 47,
    "atypical": 16,
    "6+": 12,
}

ULOVDOMOV_SITE_TYPES = {
    "studio": 1,
    "1+kk": 2,
    "1+1": 3,
    "2+kk": 4,
    "2+1": 5,
    "3+kk": 6,
    "3+1": 7,
    "4+kk": 8,
    "4+1": 9,
    "atypical": 16,
    "house": 29,
    "room": 28
}
