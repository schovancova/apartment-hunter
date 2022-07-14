"""https://www.bezrealitky.cz/"""
from datetime import datetime


class BezRealitkyApartment:
    """Representation of apartment on bezrealitky"""

    def __init__(self, ap):
        self.id = ap["id"]
        self.url = f"https://www.bezrealitky.cz/nemovitosti-byty-domy/{ap['uri']}"
        self.disposition = ap["disposition"]
        self.price = ap["price"] + ap["charges"]
        self.estate_type = ap["offerType"]
        self.size = ap["surface"]
        self.size_land = ap["surfaceLand"]
        self.tags = str(ap['tags'])
        self.address = ap['address']

    @property
    def all(self):
        """All attributes"""
        return self.__dict__
