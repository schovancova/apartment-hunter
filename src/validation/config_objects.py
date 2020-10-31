"""Validation objects"""
import re


class ConfigBase:
    def __init__(self, required=False):
        self.required = required

    def validate(self, value):
        if value != 0 and self.required and not value:
            raise ValueError(f"Missing value")


class ConfigBool(ConfigBase):
    """Config boolean value"""
    def __init__(self, required=False):
        super().__init__(required)

    def validate(self, value):
        """Validate"""
        super().validate(value)
        if value not in ["true", "false"]:
            raise ValueError(f"Invalid bool value: {value}")


class ConfigInt(ConfigBase):
    """Config integer value"""
    def __init__(self, required=False):
        super().__init__(required)

    def validate(self, value):
        """Validate"""
        super().validate(value)
        try:
            int(value)
        except ValueError:
            raise ValueError(f"Invalid integer value: {value}")


class ConfigList(ConfigBase):
    """Config list value"""
    def __init__(self, allowed, separator, required=False):
        super().__init__(required)
        self.allowed = allowed
        self.separator = separator

    def validate(self, value):
        """Validate"""
        super().validate(value)
        for val in value.split(self.separator):
            if val not in self.allowed:
                raise ValueError(f"Invalid value: {val} (allowed are {self.allowed})")


class ConfigString(ConfigBase):
    """Config string value"""
    def __init__(self, required=False, regex=None, allowed=None):
        super().__init__(required)
        self.regex = regex
        self.allowed = allowed

    def validate(self, value):
        """Validate"""
        super().validate(value)
        if self.regex and not re.match(self.regex, value):
            raise ValueError(f"Invalid value: {value}")
        if self.allowed and value not in self.allowed:
            raise ValueError(f"Invalid value: {value} (allowed are {self.allowed})")
