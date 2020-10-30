"""Config validator"""


class ConfigBool:
    """Config boolean value"""
    @staticmethod
    def validate(value):
        """Validate"""
        try:
            bool(value)
        except ValueError:
            raise ValueError(f"Invalid bool value: {value}")


class ConfigInt:
    """Config integer value"""
    @staticmethod
    def validate(value):
        """Validate"""
        try:
            int(value)
        except ValueError:
            raise ValueError(f"Invalid integer value: {value}")


class ConfigList:
    """Config list value"""
    def __init__(self, allowed, separator):
        self.allowed = allowed
        self.separator = separator

    def validate(self, value):
        """Validate"""
        for val in value.split(self.separator):
            if val not in self.allowed:
                raise ValueError(f"Invalid value: {val} (allowed are {self.allowed})")


class ConfigValue:
    """Config single value"""
    def __init__(self, allowed):
        self.allowed = allowed

    def validate(self, value):
        """Validate"""
        if value not in self.allowed:
            raise ValueError(f"Invalid value: {value} (allowed are {self.allowed})")


ULOVDOMOV_TYPES = ["studio", "1+1", "2+1", "3+1", "4+1", "1+kk", "2+kk",
                   "3+kk", "4+kk", "atypical", "house", "5+", "room"]
BEZREALITKY_TYPES = ["studio", "1+1", "2+1", "3+1", "4+1", "1+kk", "2+kk", "3+kk", "4+kk",
                     "5+1", "5+kk", "6+1", "6+kk", "7+kk", "7+1", "other"]
OFFER_TYPES = ["rent", "sharing", "sale"]
ESTATE_TYPES = ["flat"]

VALIDATORS = {
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
    """Validate config file"""
    error_msgs = []
    for site in config.sections():
        for (key, value) in config.items(site):
            try:
                validator = VALIDATORS[site][key]
                try:
                    validator.validate(value)
                except ValueError as ex:
                    error_msgs.append(f"{site}: {key} : {str(ex)}")
            except KeyError:
                error_msgs.append(f"{site}: Unrecognized key: {key}")
    if error_msgs:
        exit("\n".join(error_msgs))
