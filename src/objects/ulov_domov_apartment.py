"""https://www.ulovdomov.cz/"""
from datetime import datetime as dt


class UlovDomovApartment:
    """Representation of apartment on ulovdomov"""
    def __init__(self, ap):
        self.conveniences_url = "https://www.ulovdomov.cz/fe-api/common/conveniences"
        self.id = ap["id"]
        self.url = ap["absolute_url"]
        self.size = ap["acreage"]
        self.disposition_id = ap["disposition_id"]
        self.price = ap["price_rental"]
        self.street = ap["street"]["label"]
        self.city = ap["village_part"]["label"]
        self.published = ap["published_at"]
        self.commission = ap["price_commission"]
        self.monthly_fee = ap["price_monthly_fee"]
        self.price_note = ap['price_note']
        self.conveniences = ap['conveniences']

    def format_publish_date(self):
        """Format publish date into universal format"""
        if not self.published:
            return ""
        return dt.strptime(self.published, "%Y-%m-%dT%H:%M:%S+%f").strftime("%d.%m. %Y %H:%M")

    def format_conveniences(self):
        """Formats conveniences into a string"""
        return ", ".join(self.conveniences)

    @property
    def all(self):
        """All attributes"""
        return self.__dict__
