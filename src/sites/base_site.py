"""One site to rule them all"""
from tinydb import Query


class BaseSite:
    def __init__(self, price_min=None, price_max=None, size_min=None, size_max=None,
                 types=None, radius=5, city="Brno", active=True):
        self.price_min = price_min
        self.price_max = price_max
        self.size_min = size_min
        self.size_max = size_max
        self.types = types
        self.radius = int(radius)
        self.city = city
        self.active = active
        self.site = ""

    def save_apartment_into_db(self, db, id):
        db.insert({"id": id, 'site': self.site})

    def is_in_db(self, db, id):
        apartment = Query()
        return db.search((apartment.id == id) & (apartment.site == self.site))
