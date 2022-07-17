"""https://www.sreality.cz/"""
from src.utils.constants import SREALITY_SITE_TYPES


def index_to_disposition(index):
    """Sreality uses indexes instead of dispositions"""
    translations = {str(v): k for k, v in SREALITY_SITE_TYPES.items()}
    return translations.get(str(index), "")


class SrealityApartment:
    """Representation of apartment on sreality"""

    def __init__(self, ap):
        disposition = index_to_disposition(ap["seo"]["category_sub_cb"])
        self.id = ap['seo']['locality']
        self.name = ap["name"]
        self.url = f"https://www.sreality.cz/detail/pronajem/byt/{disposition}/{ap['seo']['locality']}/{self.id}"
        self.disposition = disposition
        self.price = ap["price"]
        self.tags = str(ap['labels'])
        self.address = ap['locality']

    @property
    def all(self):
        """All attributes"""
        return self.__dict__
