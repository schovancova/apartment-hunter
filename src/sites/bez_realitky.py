"""https://www.bezrealitky.cz/"""
import json
import re

import requests
from src.objects.bez_realitky_apartment import BezRealitkyApartment
import src.utils.constants as const
from src.sites.base_site import BaseSite


class BezRealitky(BaseSite):
    """Bezrealitky site operator"""
    def __init__(self, price_min=None, price_max=None, size_min=None, size_max=None,
                 offer_type=None, types=None, estate_type=None, radius=5, city="Brno", enabled=True):
        super().__init__(price_min, price_max, size_min, size_max, types, radius, city, enabled)
        self.base_url = None
        self.price_max += 5000  # bezrealitky counts total price
        if not self.enabled:
            return
        self.site = const.BEZREALITKY_NAME
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
            "flat": "BYT",
            "house": "DUM",
        }.get(self.estate_type)

    @staticmethod
    def get_build_id():
        """This apparently changes every hour or so"""
        response = requests.get("https://www.bezrealitky.cz/")
        id_string = re.findall(r'buildId":"\w*"', response.text)[0]
        return id_string.replace('"', "").split(':')[-1]

    def transform_offer_type(self):
        """Transform filter offer type into site API offer type"""
        return {
            "sale": "PRODEJ",
            "rent": "PRONAJEM"
        }.get(self.offer_type)

    def transform_types_into_site_types(self):
        """Transform filter types into site API types"""
        site_types = {
            "studio": "GARSONIERA",
            "other": "OSTATNI"
        }
        result = []
        for disposition in self.types.split(","):
            if "kk" in disposition:
                num = int(disposition.split("+")[0])
                result.append(f"DISP_{num}_KK")
            elif "+" in disposition:
                num = int(disposition.split("+")[0])
                result.append(f"DISP_{num}_1")
            else:
                result.append(site_types.get(disposition, disposition))
        return "/".join(result)

    def update_api_url(self):
        build_id = self.get_build_id()
        self.base_url = f"https://www.bezrealitky.cz/_next/data/{build_id}/cs/search.json"

    def build_payload(self):
        """Build API payload"""
        payload = {
            "offerType": self.offer_type,
            "estateType": self.estate_type,
            "priceFrom": self.price_min,
            "priceTo": self.price_max,
            "disposition": self.types,
            "surfaceFrom": self.size_min,
            "surfaceTo": self.size_max,
            "regionOsmId": "R442273",  # hardcoded for Brno for now
            "osm_value": "Brno",  # hardcoded for Brno for now
            "order": "TIMEORDER_DESC"
        }
        return {k: v for k, v in payload.items() if v}

    def get_new_apartments(self):
        """Get new apartment objects"""
        self.update_api_url()  # it constantly changes due to build IDs in URL
        payload = self.build_payload()
        req = requests.get(self.base_url, headers=const.HEADERS, params=payload)
        content = json.loads(req.content)
        return [BezRealitkyApartment(ap) for ap in content['pageProps']['listAdverts']]

    @staticmethod
    def get_email_message(ap):
        """Build email message"""
        disp = ap.disposition.replace("DISP_", "").replace("_", "+")
        subject = f"*{disp}*  {ap.size}m2, {ap.price} + {ap.monthly_costs} Kč @ {ap.address}"
        body = f"""\n
        * *Price full*: {ap.price + ap.monthly_costs} Kc
        * *Price/m2 (rent only)*: {int(ap.price/ap.size)}
        * *Conveniences*: {ap.format_conveniences()}
        * *Photo*: <{ap.image}|image>
        """
        return subject, body
