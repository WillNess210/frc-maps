from .CityDataset import CityDataset
from .ZipCodeDataset import ZipCodeDataset  
from typing import List, Optional

class CountyCodeFetcher:
    def __init__(self, city_dataset: CityDataset, zipcode_dataset: ZipCodeDataset):
        self.__city_dataset = city_dataset
        self.__zipcode_dataset = zipcode_dataset

    def get_county_codes(self, city_name: str, state_name: str, zipcode: str) -> Optional[List[str]]:
        city = self.__city_dataset.get_city(city_name, state_name)
        if city is not None:
            return [city.get_county_code()]
        zipcodes = self.__zipcode_dataset.get_zipcodes(zipcode)
        if zipcodes is not None:
            return [zipcode.get_county_code() for zipcode in zipcodes]
        
        return None