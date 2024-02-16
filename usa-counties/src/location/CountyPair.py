from . import CountyLocation
from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    Source: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r


class CountyPair:
    def __init__(self, county_one: CountyLocation, county_two: CountyLocation):
        self.__county_one = county_one
        self.__county_two = county_two
        self.__distance = self.__calculate_distance()

    def __calculate_distance(self) -> float:
        county_one_latitude = self.__county_one.get_latitude()
        county_one_longitude = self.__county_one.get_longitude()
        county_two_latitude = self.__county_two.get_latitude()
        county_two_longitude = self.__county_two.get_longitude()
        return haversine(
            float(county_one_longitude),
            float(county_one_latitude),
            float(county_two_longitude),
            float(county_two_latitude),
        )

    def get_distance(self) -> float:
        return self.__distance

    def get_county_one(self) -> CountyLocation:
        return self.__county_one

    def get_county_two(self) -> CountyLocation:
        return self.__county_two

    def __str__(self):
        return f"CountyDistance({self.__county_one.get_county_fips()}, {self.__county_two.get_county_fips()}, {self.__distance})"
