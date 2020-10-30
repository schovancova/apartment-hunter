"""https://www.bezrealitky.cz/"""
import json
import requests
import math
from datetime import datetime as dt
from src.utils.common import get_bounding_box
from bs4 import BeautifulSoup
from tinydb import Query


class BezRealitkyApartment:
    def __init__(self, ap):
        self.id = ap["id"]
        self.url = f"https://www.bezrealitky.cz/nemovitosti-byty-domy/{ap['uri']}"
        self.published = ap["timeOrder"]["date"]
        ap = ap["advertEstateOffer"][0]
        self.disposition = ap["keyDisposition"]
        self.price = ap["price"]
        #self.street = ap["street"]["label"]
        #self.city = ap["village_part"]["label"]
        self.estate_type = ap["keyEstateType"]
        self.size = ap["surface"]
        self.size_land = ap["surfaceLand"]

    def format_publish_date(self):
        if not self.published:
            return ""
        return dt.strptime(self.published, "%Y-%m-%d %H:%M:%S.%f").strftime("%d.%m. %Y %H:%M")


    @property
    def all(self):
        return self.__dict__
