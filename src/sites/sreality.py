"""https://www.sreality.cz/"""
import json
import requests
import src.utils.constants as const
from src.objects.sreality_apartment import SrealityApartment
from src.sites.base_site import BaseSite


class Sreality(BaseSite):
    """Sreality site operator"""
    def __init__(self, price_min=None, price_max=None, size_min=None, size_max=None,
                 offer_type=None, types=None, estate_type=None, radius=5, city="Brno", enabled=True):
        super().__init__(price_min, price_max, size_min, size_max, types, radius, city, enabled)
        if not self.enabled:
            return
        self.site = const.SREALITY_NAME
        self.base_url = "https://www.sreality.cz/api/cs/v2/estates"
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
            "flat": "1",
            "house": "2",
        }.get(self.estate_type)

    def transform_offer_type(self):
        """Transform filter offer type into site API offer type"""
        return {
            "sale": "3",
            "rent": "2"
        }.get(self.offer_type)

    def transform_types_into_site_types(self):
        """Transform filter types into site API types"""
        result = []
        for disposition in self.types.split(","):
            result.append(const.SREALITY_SITE_TYPES.get(disposition, disposition))
        return "|".join(map(str, result))

    def build_payload(self):
        """Build API payload"""
        payload = {
            "category_main_cb": self.estate_type,  # house/flat
            "category_sub_cb": self.types,  # dispositions
            "category_type_cb": self.offer_type,  # sale or rent
            "czk_price_summary_order2": "|".join([str(self.price_min), str(self.price_max)]),
            "locality_district_id": 72,  # hardcoded Brno
            "locality_region_id": 14,  # hardcoded Brno
            "page": 1,
            "per_page": 20,
            "usable_area": "|".join([str(self.size_min), str(self.size_max)])
        }
        return {k: v for k, v in payload.items() if v}

    def get_new_apartments(self):
        """Get new apartment objects"""
        payload = self.build_payload()
        req = requests.get(self.base_url, headers=const.HEADERS, params=payload)
        content = json.loads(req.content)
        # ignore region tips that are usually irrelevant
        return [SrealityApartment(ap) for ap in content['_embedded']['estates'] if ap['region_tip'] == 0]

    @staticmethod
    def get_email_message(ap):
        """Build email message"""
        subject = f"*{ap.name}*, {ap.price} Kč + fees @ {ap.address}"
        body = f"""\n
       * *Price/m2 (rent only)*: {int(ap.price / ap.size)}
       * *Conveniences*: {ap.format_conveniences()}
       * *Photo*: {ap.image}
       """
        return subject, body
