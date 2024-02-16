class CountyLocation:
    def __init__(self, county_fips, latitude, longitude):
        self.__county_fips = county_fips
        self.__latitude = latitude
        self.__longitude = longitude

    def get_county_fips(self) -> str:
        return self.__county_fips

    def get_latitude(self) -> str:
        return self.__latitude

    def get_longitude(self) -> str:
        return self.__longitude

    def __str__(self):
        return f"CountyLocation({self.__county_fips}, {self.__latitude}, {self.__longitude})"
