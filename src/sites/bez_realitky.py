"""https://www.bezrealitky.cz/"""
import json
import requests
from src.objects.bez_realitky_apartment import BezRealitkyApartment
import src.utils.constants as const
from src.sites.base_site import BaseSite


class BezRealitky(BaseSite):
    """Bezrealitky site operator"""
    def __init__(self, price_min=None, price_max=None, size_min=None, size_max=None,
                 offer_type=None, types=None, estate_type=None, radius=5, city="Brno", enabled=True):
        super().__init__(price_min, price_max, size_min, size_max, types, radius, city, enabled)
        if not self.enabled:
            return
        self.site = const.BEZREALITKY_NAME
        self.base_url = "https://www.bezrealitky.cz/_next/data/84971a3f10bdc929aa9e0caefb226898e96b2e10/cs/search.json"
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
        payload = self.build_payload()
        req = requests.get(self.base_url, headers=const.HEADERS, params=payload)
        content = json.loads(req.content)
        return [BezRealitkyApartment(ap) for ap in content['pageProps']['listAdverts']]

    @staticmethod
    def get_email_message(ap):
        """Build email message"""
        disp = ap.disposition.replace("DISP_", "").replace("_","+")
        subject = f"{disp} {ap.size} m2, {ap.price} Kč @ {ap.address}"
        body = f"""\
            {ap.url}
            Price: {ap.price} Kc,
            Land: {ap.size} m2,
            """
        return subject, body
