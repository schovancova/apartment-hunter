"""One site to rule them all"""
from datetime import datetime


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

    def save_apartment_into_db(self, database, apartment_id, apartment_url):
        """Save into db"""
        now = datetime.now()
        compound_id = f"{self.site}-{apartment_id}"
        database.collection("apartments").document(compound_id).set(
            {'url': apartment_url, 'timestamp': now.strftime("%d.%m. %Y, %H:%M:%S")})

    def is_in_db(self, database, apartment_id):
        """Check for presence in db"""
        compound_id = f"{self.site}-{apartment_id}"
        doc = database.collection("apartments").document(compound_id).get()
        return doc.exists
