"""https://www.ulovdomov.cz/"""
import json
import requests
from datetime import datetime as dt


class UlovDomovApartment:
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
        if not self.published:
            return ""
        return dt.strptime(self.published, "%Y-%m-%dT%H:%M:%S+%f").strftime("%d.%m. %Y %H:%M")

    def format_conveniences(self):
        req = requests.get(self.conveniences_url)
        content = json.loads(req.content)
        result = []
        for conv in content:
            if conv["id"] in self.conveniences:
                result.append(conv["label"])
        return ", ".join(result)

    @property
    def all(self):
        return self.__dict__
