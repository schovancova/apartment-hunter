"""https://www.ulovdomov.cz/"""
import json
import requests
from datetime import datetime as dt


class UlovDomov:
    def __init__(self, price_min=None, price_max=None, size_min=None, size_max=None):
        self.price_min = price_min
        self.price_max = price_max
        self.size_min = size_min
        self.size_max = size_max
        self.base_url = "https://www.ulovdomov.cz/fe-api/find?offers_only=true"

    def build_payload(self):
        return {
            "query": "Brno",
            "offer_type_id": "1",
            "dispositions": [],
            "price_from": str(self.price_min),
            "price_to": str(self.price_max),
            "acreage_from": str(self.size_min),
            "acreage_to": str(self.price_max),
            "added_before": "",
            "is_price_commision_free": False,
            "sort_by": "date:desc",
            "page": 1,
            "limit": 20,
            "bounds": {
                "north_east": {"lng": 16.749343872070316, "lat": 49.31438004800689},
                "south_west": {"lng": 16.406021118164066, "lat": 49.0900564769189}}}

    def get_new_apartments(self):
        payload = self.build_payload()
        req = requests.post(self.base_url, data=json.dumps(payload))
        content = json.loads(req.content)
        return content['offers']

    def translate_disposition(self, formal=None, informal=None):
        req = requests.get(self.disposition_url)
        content = json.loads(req.content)
        for disposition in content:
            if disposition["label"] == informal or disposition["id"] == formal:
                return disposition

    @staticmethod
    def get_email_message(raw_apartment):
        ap = UlovDomovApt(raw_apartment)
        disposition = ap.index_to_disposition()
        commission = 'yes' if ap.commission else 'no'
        subject = f"{disposition} {ap.city}, {ap.street}, {ap.price} Kč"
        body = f"""\
            {ap.url}
            Published: {ap.format_publish_date()}
            Commission: {commission}
            Monthly fee: {ap.monthly_fee},
            Price note: {ap.price_note}
            Conveniences: {ap.format_conveniences()}
            """
        return subject, body

    @staticmethod
    def save_apartment_into_db(db, ap):
        db.insert(UlovDomovApt(ap).all)


class UlovDomovApt:
    def __init__(self, ap):
        self.disposition_url = "https://www.ulovdomov.cz/fe-api/disposition/all/1"
        self.conveniences_url = "https://www.ulovdomov.cz/fe-api/common/conveniences"
        self.id = ap["id"]
        self.url = ap["absolute_url"]
        self.disposition_id = ap["disposition_id"]
        self.price = ap["price_rental"]
        self.street = ap["street"]["label"]
        self.city = ap["village_part"]["label"]
        self.published = ap["published_at"]
        self.commission = ap["price_commission"]
        self.monthly_fee = ap["price_monthly_fee"]
        self.price_note = ap['price_note']
        self.conveniences = ap['conveniences']

    def index_to_disposition(self):
        req = requests.get(self.disposition_url)
        content = json.loads(req.content)
        for disposition in content:
            if disposition["id"] == self.disposition_id:
                return disposition["label"]

    def format_publish_date(self):
        return dt.strptime(self.published, "%Y-%m-%dT%H:%M:%S+%f").strftime("%d.%m. %Y %H:%M")

    def format_conveniences(self):
        req = requests.get(self.disposition_url)
        content = json.loads(req.content)
        result = []
        for conv in content:
            if conv["id"] in self.conveniences:
                res.append(conv["label"])
        return ", ".join(result)

    @property
    def all(self):
        return self.__dict__
