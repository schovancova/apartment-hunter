"""Common functions"""
import os
import errno
import math
import logging

from geopy.geocoders import Nominatim
import configparser
from tinydb import TinyDB


def get_config(path):
    """Get config file"""
    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_db(path):
    """Get db"""
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    open(path, 'a+')
    return TinyDB(path)


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
