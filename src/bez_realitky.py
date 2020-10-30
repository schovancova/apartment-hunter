"""https://www.bezrealitky.cz/"""
import json
import requests
import math
from datetime import datetime as dt
from src.common import get_bounding_box
from bs4 import BeautifulSoup


class BezRealitky:
    def __init__(self, price_min=None, price_max=None, size_min=None, size_max=None,
                 offer_type=None, types=None, estate_type=None, **kwargs):
        self.base_url = "https://www.bezrealitky.cz/api/record/markers"
        self.price_min = price_min
        self.price_max = price_max
        self.size_min = size_min
        self.size_max = size_max
        self.offer_type = offer_type
        self.types = types
        self.estate_type = estate_type

    def build_payload(self):
        bounding_box = get_bounding_box("Brno", 10)
        formatted_box = str(json.dumps(
            [[[bounding_box["nw"], bounding_box["ne"], bounding_box["se"], bounding_box["sw"]]]]
        )).replace(" ", "")
        payload = {
            "offerType": self.offer_type,
            "estateType": self.estate_type,
            "priceFrom": self.price_min,
            "priceTo": self.price_max,
            "disposition": self.types,
            "surfaceFrom": self.size_min,
            "surfaceTo": self.size_max,
            "boundary": formatted_box
        }
        return {k: v for k, v in payload.items() if v}

    def get_new_apartments(self):
        payload = self.build_payload()
        req = requests.post(self.base_url, data=payload)
        content = json.loads(req.content)
        return content

    @staticmethod
    def get_email_message(raw_apartment):
        ap = BezRealitkyApt(raw_apartment)

        subject = f"{ap.disposition.replace('-','+')} {ap.size} m2, {ap.price} Kč"
        body = f"""\
            {ap.url}
            Published: {ap.format_publish_date()}
            Land: {ap.size_land} m2,
            """
        return subject, body

    @staticmethod
    def save_apartment_into_db(db, ap):
        db.insert(BezRealitkyApt(ap).all)


class BezRealitkyApt:
    def __init__(self, ap):
        self.id = ap["id"]
        self.url = f"https://www.bezrealitky.cz/nemovitosti-byty-domy/{ap['uri']}"
        self.published = ap["timeOrder"]["date"]
        ap = ap["advertEstateOffer"][0]
        self.disposition = ap["keyDisposition"]
        self.price = ap["price"]
        #self.street = ap["street"]["label"]
        #self.city = ap["village_part"]["label"]
        self.estate_type = ap["keyEstateType"]
        self.size = ap["surface"]
        self.size_land = ap["surfaceLand"]

    def format_publish_date(self):
        if not self.published:
            return ""
        return dt.strptime(self.published, "%Y-%m-%d %H:%M:%S.%f").strftime("%d.%m. %Y %H:%M")

    @property
    def all(self):
        return self.__dict__
