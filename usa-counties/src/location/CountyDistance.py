class CountyDistance:
    def __init__(self, county_fips, distance: float):
        self.__county_fips = county_fips
        self.__distance = distance

    def get_distance(self) -> float:
        return self.__distance

    def get_county_fips(self) -> str:
        return self.__county_fips

    def __str__(self):
        return f"CountyDistance({self.__county_fips}, {self.__distance})"
