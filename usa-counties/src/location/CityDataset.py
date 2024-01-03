import pandas as pd
from .City import City
from typing import Dict, Tuple, List, Optional

# only keeping a subset of the columns to save memory
CITY_NAME_COLUMN = 'city'
STATE_NAME_COLUMN = 'state_name'
COUNTY_CODE_COLUMN = 'county_fips'
columns: List[str] = [CITY_NAME_COLUMN, STATE_NAME_COLUMN, COUNTY_CODE_COLUMN]

class CityDataset:
    def __init__(self, filepath):
        df = pd.read_csv(filepath, usecols=columns, dtype=str)
        self.__create_lookup_map(df)
        
    def __create_lookup_map(self, df: pd.DataFrame):
        # create a map from ("city", "state_name") to City
        self.__lookup_map: Dict[Tuple[str, str], City] = {}
        for _, row in df.iterrows():
            city_name: str = row[CITY_NAME_COLUMN]
            state_name: str = row[STATE_NAME_COLUMN]
            county_code: str = row[COUNTY_CODE_COLUMN]

            key: Tuple[str, str] = (city_name, state_name)
            city = City(city_name, state_name, county_code)
            self.__lookup_map[key] = city

    def get_city(self, city_name: str, state_name: str) -> Optional[City]:
        key = (city_name, state_name)
        if key in self.__lookup_map:
            return self.__lookup_map[key]
        return None
