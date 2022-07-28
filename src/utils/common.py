"""Common functions"""
from datetime import datetime, time as datetime_time
import math
import logging

from geopy.geocoders import Nominatim
from google.cloud import firestore
import configparser

from src.utils.constants import CHECK_FREQUENCY_IN_SECONDS_NIGHT, CHECK_FREQUENCY_IN_SECONDS_DAY


def get_config(path):
    """Get config file"""
    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_db():
    """Get db"""
    return firestore.Client()


def get_logger():
    """Get logger"""
    logger = logging.getLogger('apartment_logger')
    logging.basicConfig(level=logging.INFO)
    return logger


def get_bounding_box(city, km_radius):
    """Get bounding box latitudes and logitudes (4 points making a square around the city)"""
    geo_locator = Nominatim(user_agent="apartment-hunter")
    location = geo_locator.geocode(city)
    offset = km_radius / 100.0
    lat_max = location.latitude + offset
    lat_min = location.latitude - offset

    lng_offset = offset * math.cos(location.latitude * math.pi / 180.0)
    lng_max = location.longitude + lng_offset
    lng_max_twice = location.longitude + lng_offset * 2
    lng_min = location.longitude - lng_offset
    lng_min_twice = location.longitude - lng_offset * 2
    return {
        "nw": {"lat": lat_max, "lng": lng_min_twice},
        "ne": {"lat": lat_max, "lng": lng_max},
        "sw": {"lat": lat_min, "lng": lng_min},
        "se": {"lat": lat_min, "lng": lng_max_twice},
    }


def determine_frequency():
    now = datetime.now()
    now_time = now.time()
    if now_time >= datetime_time(23, 59) or now_time <= datetime_time(6, 00):
        return CHECK_FREQUENCY_IN_SECONDS_NIGHT
    return CHECK_FREQUENCY_IN_SECONDS_DAY
