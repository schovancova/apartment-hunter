"""One site to rule them all"""
from tinydb import Query


class BaseSite:
    """Base site"""
    def __init__(self, price_min=None, price_max=None, size_min=None, size_max=None,
                 types=None, radius=5, city="Brno", enabled=True):
        self.price_min = price_min
        self.price_max = price_max
        self.size_min = size_min
        self.size_max = size_max
        self.types = types
        self.radius = int(radius)
        self.city = city
        self.enabled = True if enabled == "true" else False
        self.site = ""

    def save_apartment_into_db(self, database, apartment_id):
        """Save into db"""
        database.insert({"id": apartment_id, 'site': self.site})

    def is_in_db(self, database, apartment_id):
        """Check for presence in db"""
        apartment = Query()
        return database.search((apartment.id == apartment_id) & (apartment.site == self.site))
