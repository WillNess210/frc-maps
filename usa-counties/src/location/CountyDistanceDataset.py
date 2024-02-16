import json
from typing import Dict, List
from .CountyDistance import CountyDistance


class CountyDistanceDataset:
    def __init__(self, filepath):
        data = {}
        with open(filepath, "r") as f:
            data = json.load(f)
        self.__create_lookup_map(data)

    def __create_lookup_map(self, data: Dict[str, List]):
        self.__lookup_map: Dict[str, List[CountyDistance]] = {}
        for key, value in data.items():
            self.__lookup_map[key] = []
            for county_distance in value:
                county_fips: str = county_distance[0]
                distance: float = county_distance[1]
                county_distance = CountyDistance(county_fips, distance)
                self.__lookup_map[key].append(county_distance)

    def get_closest_counties_for_county(self, county_fips: str) -> List[CountyDistance]:
        if county_fips not in self.__lookup_map:
            raise ValueError(f"County {county_fips} not found in dataset")
        return self.__lookup_map[county_fips]
