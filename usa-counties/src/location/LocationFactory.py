from .CityDataset import CityDataset
from .ZipCodeDataset import ZipCodeDataset
from .CountyCodeFetcher import CountyCodeFetcher
from typing import Tuple
from config import CONFIG


class LocationFactory:
    def __init__(self):
        filepaths = CONFIG.get_filepaths()
        self.__city_dataset = CityDataset(filepaths.get_us_cities_filepath())
        self.__zipcode_dataset = ZipCodeDataset(filepaths.get_zipcodes_filepath())
        self.__county_code_fetcher = CountyCodeFetcher(
            self.__city_dataset, self.__zipcode_dataset
        )

    def get_county_code_fetcher(self) -> CountyCodeFetcher:
        return self.__county_code_fetcher

    def get_city_dataset(self) -> CityDataset:
        return self.__city_dataset

    def get_zipcode_dataset(self) -> ZipCodeDataset:
        return self.__zipcode_dataset

    def get_all(self) -> Tuple[CityDataset, ZipCodeDataset, CountyCodeFetcher]:
        return self.__city_dataset, self.__zipcode_dataset, self.__county_code_fetcher
