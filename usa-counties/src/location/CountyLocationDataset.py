import pandas as pd
from typing import Dict, List, Optional
from .CountyLocation import CountyLocation

# only keeping a subset of the columns to save memory
COUNTY_FIPS_COLUMN = "FIPS"
LATITUDE_COLUMN = "Latitude"
LONGITUDE_COLUMN = "Longitude"
columns: List[str] = [COUNTY_FIPS_COLUMN, LATITUDE_COLUMN, LONGITUDE_COLUMN]


class CountyLocationDataset:
    def __init__(self, filepath):
        df = pd.read_csv(filepath, usecols=columns, dtype=str)
        self.__create_lookup_map(df)

    def __create_lookup_map(self, df: pd.DataFrame):
        self.__lookup_map: Dict[str, CountyLocation] = {}
        for _, row in df.iterrows():
            county_fips: str = row[COUNTY_FIPS_COLUMN][1:]
            latitude: str = row[LATITUDE_COLUMN]
            longitude: str = row[LONGITUDE_COLUMN]
            county_location = CountyLocation(county_fips, latitude, longitude)
            self.__lookup_map[county_fips] = county_location

    def get_county_keys(self) -> List[str]:
        return list(self.__lookup_map.keys())

    def get_county_location(self, county_fips: str) -> Optional[CountyLocation]:
        if county_fips in self.__lookup_map:
            return self.__lookup_map[county_fips]
        return None
