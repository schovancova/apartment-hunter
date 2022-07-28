"""https://www.ulovdomov.cz/"""
import json
import requests
from src.objects.ulov_domov_apartment import UlovDomovApartment
from src.utils.common import get_bounding_box
import src.utils.constants as const
from src.sites.base_site import BaseSite


def index_to_disposition(index):
    """Ulovdomov uses indexes instead of dispositions"""
    translations = {str(v): k for k, v in const.ULOVDOMOV_SITE_TYPES.items()}
    return translations.get(str(index), "")


class UlovDomov(BaseSite):
    """Ulovdomov site operator"""

    def __init__(self, price_min=None, price_max=None, size_min=None, size_max=None,
                 types=None, no_commission=None, radius=5, city="Brno", enabled=True):
        super().__init__(price_min, price_max, size_min, size_max, types, radius, city, enabled)
        if not self.enabled:
            return
        self.site = const.ULOVDOMOV_NAME
        self.no_commission = True if no_commission == "true" else False
        self.base_url = "https://www.ulovdomov.cz/fe-api/find"
        if types:
            self.transform_types_into_indexes()

    def transform_types_into_indexes(self):
        """Translate filter types into API indexed types"""
        result = []
        for disposition in self.types.split(","):
            disposition = const.ULOVDOMOV_SITE_TYPES.get(disposition, disposition)
            result.append(disposition)
        self.types = list(sorted(result))

    def build_payload(self):
        """Build API payload"""
        bounding_box = get_bounding_box(self.city, self.radius)
        payload = {
            "dispositions": self.types,
            "price_from": self.price_min,
            "price_to": self.price_max,
            "acreage_from": self.size_min,
            "acreage_to": self.size_max,
            "is_price_commision_free": self.no_commission if self.no_commission else None,
            "sort_by": "date:desc",
            "page": 1,
            "limit": 20,
            "bounds": {
                "north_east": bounding_box["ne"],
                "south_west": bounding_box["sw"]}}
        result = {k: v for k, v in payload.items() if v is not None}
        result['offer_type_id'] = None  # this has to be there
        return result

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
        if ap.monthly_fee:
            fee_text = ap.monthly_fee
        else:
            fee_text = "fees"
        subject = f"*{disposition}*  {ap.size}m2, {ap.price} + {fee_text} Kč @ {ap.city}, {ap.street}"
        body = f"""\n
        * *Published*: {ap.format_publish_date()}
        * *RK Commission*: {commission}
        * *Price/m2 (rent only)*: {int(ap.price/ap.size)}
        * *Monthly fee*: {ap.monthly_fee if ap.monthly_fee else "-"}
        * *Price note*: {ap.price_note}
        * *Conveniences*: {ap.format_conveniences()}
        * *Photo*: {ap.photo}
        """
        return subject, body
