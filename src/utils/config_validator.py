
class ConfigBool:
    def __init__(self): pass

    @staticmethod
    def validate(value):
        try:
            bool(value)
        except ValueError:
            return f"Invalid bool value: {value}"


class ConfigInt:
    def __init__(self): pass

    @staticmethod
    def validate(value):
        try:
            int(value)
        except ValueError:
            return f"Invalid integer value: {value}"


class ConfigList:
    def __init__(self, allowed, separator):
        self.allowed = allowed
        self.separator = separator

    def validate(self, value):
        for val in value.split(self.separator):
            if val not in self.allowed:
                return f"Invalid value: {val} (allowed are {self.allowed})"


class ConfigValue:
    def __init__(self, allowed):
        self.allowed = allowed

    def validate(self, value):
        if value not in self.allowed:
            return f"Invalid value: {value} (allowed are {self.allowed})"


ULOVDOMOV_TYPES = ["studio", "1+1", "2+1", "3+1", "4+1", "1+kk", "2+kk",
                   "3+kk", "4+kk", "atypical", "house", "5+", "room"]
BEZREALITKY_TYPES = ["studio", "1+1", "2+1", "3+1", "4+1", "1+kk", "2+kk", "3+kk", "4+kk",
                     "5+1", "5+kk", "6+1", "6+kk", "7+kk", "7+1", "other"]
OFFER_TYPES = ["rent", "sharing", "sale"]
ESTATE_TYPES = ["flat"]

validators = {
    "ulov_domov": {
        "city": ConfigValue(allowed=["Brno"]),
        "radius": ConfigInt(),
        "active": ConfigBool(),
        "price_min": ConfigInt(),
        "price_max": ConfigInt(),
        "size_max": ConfigInt(),
        "size_min": ConfigInt(),
        "types": ConfigList(separator=",", allowed=ULOVDOMOV_TYPES),
        "no_commission": ConfigBool(),
    },
    "bez_realitky": {
        "city": ConfigValue(allowed=["Brno"]),
        "radius": ConfigInt(),
        "active": ConfigBool(),
        "estate_type": ConfigValue(allowed=ESTATE_TYPES),
        "offer_type": ConfigValue(allowed=OFFER_TYPES),
        "price_min": ConfigInt(),
        "price_max": ConfigInt(),
        "size_max": ConfigInt(),
        "size_min": ConfigInt(),
        "types": ConfigList(separator=",", allowed=BEZREALITKY_TYPES),
    }
}


def validate_config(config):
    error_msgs = []
    for site in config.sections():
        for (key, value) in config.items(site):
            try:
                validator = validators[site][key]
                error_msg = validator.validate(value)
                if error_msg:
                    error_msgs.append(f"{site}: {key} : {error_msg}")
            except KeyError:
                error_msgs.append(f"{site}: Unrecognized key: {key}")
    if error_msgs:
        exit("\n".join(error_msgs))

