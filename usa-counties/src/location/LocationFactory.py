from .CityDataset import CityDataset
from .ZipCodeDataset import ZipCodeDataset
from .CountyCodeFetcher import CountyCodeFetcher
from typing import Tuple

us_cities_filepath = "../assets/uscities.csv"
zipcodes_filepath = "../assets/ZIP-COUNTY-FIPS_2017-06.csv"

class LocationFactory:
    def __init__(self):
        self.__city_dataset = CityDataset(us_cities_filepath)
        self.__zipcode_dataset = ZipCodeDataset(zipcodes_filepath)
        self.__county_code_fetcher = CountyCodeFetcher(self.__city_dataset, self.__zipcode_dataset)

    def get_county_code_fetcher(self) -> CountyCodeFetcher:
        return self.__county_code_fetcher
    
    def get_city_dataset(self) -> CityDataset:
        return self.__city_dataset
    
    def get_zipcode_dataset(self) -> ZipCodeDataset:
        return self.__zipcode_dataset
    
    def get_all(self) -> Tuple[CityDataset, ZipCodeDataset, CountyCodeFetcher]:
        return self.__city_dataset, self.__zipcode_dataset, self.__county_code_fetcher