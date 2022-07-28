"""https://www.bezrealitky.cz/"""


class BezRealitkyApartment:
    """Representation of apartment on bezrealitky"""

    def __init__(self, ap):
        self.id = ap["id"]
        self.url = f"https://www.bezrealitky.cz/nemovitosti-byty-domy/{ap['uri']}"
        self.disposition = ap["disposition"]
        self.price = ap["price"]
        self.estate_type = ap["offerType"]
        self.size = ap["surface"]
        self.size_land = ap["surfaceLand"]
        self.tags = ap['tags']
        self.address = ap['address']
        self.monthly_costs = ap['charges']
        self.image = ap['mainImage']['url']

    def format_conveniences(self):
        """Formats conveniences into a string"""
        return ", ".join(self.tags)

    @property
    def all(self):
        """All attributes"""
        return self.__dict__
