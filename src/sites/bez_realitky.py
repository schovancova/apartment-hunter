"""https://www.bezrealitky.cz/"""
import json
import requests
from src.utils.common import get_bounding_box
from src.objects.bez_realitky_apartment import BezRealitkyApartment
import src.utils.constants as const
from src.sites.base_site import BaseSite


class BezRealitky(BaseSite):
    """Bezrealitky site operator"""
    def __init__(self, price_min=None, price_max=None, size_min=None, size_max=None,
                 offer_type=None, types=None, estate_type=None, radius=5, city="Brno", active=True):
        super().__init__(price_min, price_max, size_min, size_max, types, radius, city, active)
        self.site = const.BEZREALITKY_NAME
        self.base_url = "https://www.bezrealitky.cz/api/record/markers"
        self.offer_type = offer_type
        self.estate_type = estate_type
        if offer_type:
            self.offer_type = self.transform_offer_type()
        if types:
            self.types = self.transform_types_into_site_types()
        if estate_type:
            self.estate_type = self.transform_estate_type()

    def transform_estate_type(self):
        """Transform filter estate type into site API estate type"""
        return {
            "flat": "byt",
            "house": "dum",
        }.get(self.estate_type)

    def transform_offer_type(self):
        """Transform filter offer type into site API offer type"""
        return {
            "sale": "prodej",
            "rent": "pronajem",
            "sharing": "spolubydleni"
        }.get(self.offer_type)

    def transform_types_into_site_types(self):
        """Transform filter types into site API types"""
        site_types = {
            "studio": "garsoniera",
            "other": "ostatni"
        }
        result = []
        for disposition in self.types.split(","):
            if "kk" in disposition or "+" in disposition:
                result.append(disposition.replace("+", "-"))
            else:
                result.append(site_types.get(disposition, disposition))
        return ",".join(result)

    def build_payload(self):
        """Build API payload"""
        bounding_box = get_bounding_box(self.city, self.radius)
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
        """Get new apartment objects"""
        payload = self.build_payload()
        req = requests.post(self.base_url, data=payload)
        content = json.loads(req.content)
        return [BezRealitkyApartment(ap) for ap in content]

    @staticmethod
    def get_email_message(ap):
        """Build email message"""
        subject = f"{ap.disposition.replace('-','+')} {ap.size} m2, {ap.price} Kč"
        body = f"""\
            {ap.url}
            Published: {ap.format_publish_date()}
            Land: {ap.size_land} m2,
            """
        return subject, body
