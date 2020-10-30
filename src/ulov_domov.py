"""https://www.ulovdomov.cz/"""
import json
import requests
from datetime import datetime as dt

disposition_url = "https://www.ulovdomov.cz/fe-api/disposition/filter-only/1"


def index_to_disposition(index):
    req = requests.get(disposition_url)
    content = json.loads(req.content)
    for disposition in content:
        if disposition["id"] == index:
            return disposition["label"]


def disposition_to_index(disp):
    req = requests.get(disposition_url)
    content = json.loads(req.content)
    for disposition in content:
        if disposition["label"] == disp:
            return disposition["id"]
    raise ValueError(f"{disp} disposition for UlovDomov is not supported")


class UlovDomov:
    def __init__(self, price_min=None, price_max=None, size_min=None, size_max=None, types=None):
        self.price_min = price_min
        self.price_max = price_max
        self.size_min = size_min
        self.size_max = size_max
        self.types = types
        self.base_url = "https://www.ulovdomov.cz/fe-api/find?offers_only=true"
        if types:
            self.transform_types_into_indexes()

    def transform_types_into_indexes(self):
        result = []
        for disposition in self.types.split(","):
            result.append(disposition_to_index(disposition.strip()))
        self.types = list(map(str, sorted(result)))

    def build_payload(self):
        return {
            "query": "Brno",
            "offer_type_id": "1",
            "dispositions": self.types,
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

    @staticmethod
    def get_email_message(raw_apartment):
        ap = UlovDomovApt(raw_apartment)
        disposition = index_to_disposition(ap.disposition_id)
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

    def format_publish_date(self):
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
