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
        self.id = ap['hash_id']
        self.name = ap["name"]
        self.size = self.get_size()
        self.url = f"https://www.sreality.cz/detail/pronajem/byt/{disposition}/{ap['seo']['locality']}/{ap['hash_id']}"
        self.disposition = disposition
        self.price = ap["price"]
        self.tags = ap['labels']
        self.address = ap['locality']
        if len(ap['_links']['images']) > 0:
            self.image = ap['_links']['images'][0]['href']
        else:
            self.image = ""

    def format_conveniences(self):
        """Formats conveniences into a string"""
        return ", ".join(self.tags)

    def get_size(self):
        clean_name = ''.join([i if ord(i) < 128 else ' ' for i in self.name])  # remove special chars
        parts = clean_name.split(" ")
        m_index = parts.index("m")  # index of m2
        size = parts[m_index - 1]  # size is preceding m2
        return int(size)

    @property
    def all(self):
        """All attributes"""
        return self.__dict__
