"""https://www.bezrealitky.cz/"""
from datetime import datetime


class BezRealitkyApartment:
    """Representation of apartment on bezrealitky"""
    def __init__(self, ap):
        self.id = ap["id"]
        self.url = f"https://www.bezrealitky.cz/nemovitosti-byty-domy/{ap['uri']}"
        self.published = ap["timeOrder"]["date"]
        ap = ap["advertEstateOffer"][0]
        self.disposition = ap["keyDisposition"]
        self.price = ap["price"]
        self.estate_type = ap["keyEstateType"]
        self.size = ap["surface"]
        self.size_land = ap["surfaceLand"]

    def format_publish_date(self):
        """Format publish date into universal format"""
        if not self.published:
            return ""
        return datetime.strptime(self.published, "%Y-%m-%d %H:%M:%S.%f").strftime("%d.%m. %Y %H:%M")

    @property
    def all(self):
        """All attributes"""
        return self.__dict__
