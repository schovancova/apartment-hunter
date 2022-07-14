from src.utils.constants import EMAIL_REGEX
from src.validation.config_objects import *

ULOVDOMOV_TYPES = ["studio", "1+1", "2+1", "3+1", "4+1", "1+kk", "2+kk",
                   "3+kk", "4+kk", "atypical", "house", "5+", "room"]
BEZREALITKY_TYPES = ["studio", "1+1", "2+1", "3+1", "4+1", "1+kk", "2+kk", "3+kk", "4+kk",
                     "5+1", "5+kk", "6+1", "6+kk", "7+kk", "7+1", "other"]
SREALITY_TYPES = ["1+1", "2+1", "3+1", "4+1", "5+1", "1+kk", "2+kk", "3+kk", "4+kk", "5+kk",
                  "room", "atypical", "6+"]
OFFER_TYPES = ["rent", "sharing", "sale"]
ESTATE_TYPES = ["flat"]

SITES_VALIDATORS = {
    "ulov_domov": {
        "city": ConfigString(allowed=["Brno"]),
        "radius": ConfigInt(),
        "enabled": ConfigBool(),
        "price_min": ConfigInt(),
        "price_max": ConfigInt(),
        "size_max": ConfigInt(),
        "size_min": ConfigInt(),
        "types": ConfigList(separator=",", allowed=ULOVDOMOV_TYPES),
        "no_commission": ConfigBool(),
    },
    "bez_realitky": {
        "city": ConfigString(allowed=["Brno"]),
        "radius": ConfigInt(),
        "enabled": ConfigBool(),
        "estate_type": ConfigString(allowed=ESTATE_TYPES),
        "offer_type": ConfigString(allowed=OFFER_TYPES),
        "price_min": ConfigInt(),
        "price_max": ConfigInt(),
        "size_max": ConfigInt(),
        "size_min": ConfigInt(),
        "types": ConfigList(separator=",", allowed=BEZREALITKY_TYPES),
    },
    "sreality": {
        "city": ConfigString(allowed=["Brno"]),
        "enabled": ConfigBool(),
        "estate_type": ConfigString(allowed=ESTATE_TYPES),
        "offer_type": ConfigString(allowed=OFFER_TYPES),
        "price_min": ConfigInt(),
        "price_max": ConfigInt(),
        "size_max": ConfigInt(),
        "size_min": ConfigInt(),
        "types": ConfigList(separator=",", allowed=SREALITY_TYPES),
    }
}

NOTIFICATION_VALIDATORS = {
    "email": {
        "enabled": ConfigBool(required=True),
        "sender": ConfigString(required=True, regex=EMAIL_REGEX),
        "receiver": ConfigString(required=True, regex=EMAIL_REGEX),
        "smtp_server": ConfigString(required=True),
        "smtp_port": ConfigInt(required=True)
    },
    "gmail": {
        "enabled": ConfigBool(required=True),
        "sender": ConfigString(required=True, regex=EMAIL_REGEX),
        "receiver": ConfigString(required=True, regex=EMAIL_REGEX),
    },
    "pushbullet": {
        "enabled": ConfigBool(required=True),
    },
    "slack": {
        "enabled": ConfigBool(required=True),
    }
}