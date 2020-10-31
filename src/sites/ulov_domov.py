"""https://www.ulovdomov.cz/"""
import json
import requests
from src.objects.ulov_domov_apartment import UlovDomovApartment
from src.utils.common import get_bounding_box
import src.utils.constants as const
from src.sites.base_site import BaseSite

disposition_url = "https://www.ulovdomov.cz/fe-api/disposition/filter-only/1"


def index_to_disposition(index):
    """Ulovdomov uses indexes instead of dispositions"""
    req = requests.get(disposition_url, headers=const.HEADERS)
    content = json.loads(req.content)
    for disposition in content:
        if disposition["id"] == index:
            return disposition["label"]


def disposition_to_index(disp):
    """Ulovdomov uses indexes instead of dispositions"""
    req = requests.get(disposition_url, headers=const.HEADERS)
    content = json.loads(req.content)
    for disposition in content:
        if disposition["label"] == disp:
            return disposition["id"]
    raise ValueError(f"{disp} disposition for UlovDomov is not supported")


class UlovDomov(BaseSite):
    """Ulovdomov site operator"""
    def __init__(self, price_min=None, price_max=None, size_min=None, size_max=None,
                 types=None, no_commission=None, radius=5, city="Brno", enabled=True):
        super().__init__(price_min, price_max, size_min, size_max, types, radius, city, enabled)
        if not self.enabled:
            return
        self.site = const.ULOVDOMOV_NAME
        self.no_commission = True if no_commission == "true" else False
        self.base_url = "https://www.ulovdomov.cz/fe-api/find?offers_only=true"
        if types:
            self.transform_types_into_indexes()

    def transform_types_into_indexes(self):
        """Translate filter types into API indexed types"""
        site_types = {
            "studio": "garsonka",
            "atypical": "atypický",
            "5+": "5 a větší",
            "house": "dům",
            "room": "Sdílený pokoj"
        }
        result = []
        for disposition in self.types.split(","):
            disposition = site_types.get(disposition, disposition)
            result.append(disposition_to_index(disposition.strip()))
        self.types = list(map(str, sorted(result)))

    def build_payload(self):
        """Build API payload"""
        bounding_box = get_bounding_box(self.city, self.radius)
        payload = {
            "query": "Brno",
            "offer_type_id": "1",
            "dispositions": self.types,
            "price_from": self.price_min,
            "price_to": self.price_max,
            "acreage_from": self.size_min,
            "acreage_to": self.price_max,
            "added_before": "",
            "is_price_commission_free": self.no_commission,
            "sort_by": "date:desc",
            "page": 1,
            "limit": 20,
            "bounds": {
                "north_east": bounding_box["ne"],
                "south_west": bounding_box["sw"]}}
        return {k: v for k, v in payload.items() if v is not None}

    def get_new_apartments(self):
        """Get new apartment objects"""
        payload = self.build_payload()
        req = requests.post(self.base_url, headers=const.HEADERS, data=json.dumps(payload))
        content = json.loads(req.content)['offers']
        return [UlovDomovApartment(ap) for ap in content]

    @staticmethod
    def get_email_message(ap):
        """Get email message text"""
        disposition = index_to_disposition(ap.disposition_id)
        commission = 'yes' if ap.commission else 'no'
        subject = f"{disposition} {ap.size}m2 {ap.city}, {ap.street}, {ap.price} Kč"
        body = f"""\
            {ap.url}
            Published: {ap.format_publish_date()}
            Commission: {commission}
            Monthly fee: {ap.monthly_fee},
            Price note: {ap.price_note}
            Conveniences: {ap.format_conveniences()}
            """
        return subject, body
