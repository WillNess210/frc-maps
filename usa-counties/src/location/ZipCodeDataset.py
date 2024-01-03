import pandas as pd
from .ZipCode import ZipCode
from typing import Dict, Tuple, List, Optional

ZIPCODE_COLUMN = "ZIP"
COUNTY_CODE_COLUMN = "STCOUNTYFP"
columns: List[str] = [ZIPCODE_COLUMN, COUNTY_CODE_COLUMN]

class ZipCodeDataset:
    def __init__(self, filepath):
        df = pd.read_csv(filepath, usecols=columns, dtype=str)
        self.__create_lookup_map(df)

    def __create_lookup_map(self, df: pd.DataFrame):
        # create a map from zipcode -> ZipCode
        self.__lookup_map: Dict[str, List[ZipCode]] = {}
        for _, row in df.iterrows():
            zipcode: str = row[ZIPCODE_COLUMN]
            county_code: str = row[COUNTY_CODE_COLUMN]

            zip_code = ZipCode(zipcode, county_code)
            if zipcode in self.__lookup_map:
                self.__lookup_map[zipcode].append(zip_code)
            else:
                self.__lookup_map[zipcode] = [zip_code]

    def get_zipcodes(self, zipcode: str) -> Optional[List[ZipCode]]:
        if zipcode in self.__lookup_map:
            return self.__lookup_map[zipcode]
        return None