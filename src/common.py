from geopy.geocoders import Nominatim
import math


def get_bounding_box(city, km_radius):
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
