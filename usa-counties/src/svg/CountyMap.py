from lxml import etree
from typing import List, Callable, Dict, Optional
from .County import County
import os
from config import CONFIG


class CountyMap:
    def __init__(self):
        self.svg_root = etree.parse(
            CONFIG.get_filepaths().get_usa_counties_svg_filepath()
        ).getroot()
        self.g_root = self.svg_root[2]

    def __get_counties(self):
        if hasattr(self, "counties"):
            return self.counties
        counties: List[County] = []
        county_code_to_county_dict: Dict[str, County] = {}
        for state in self.g_root:
            for county in state:
                county_obj = County(county)
                counties.append(county_obj)
                county_code_to_county_dict[county_obj.get_fips()] = county_obj
        self.counties = counties
        self.county_code_to_county_dict = county_code_to_county_dict
        return self.counties

    def for_each_county(self, func: Callable[[County], None]):
        for county in self.__get_counties():
            func(county)

    def get_county(self, county_code: str) -> Optional[County]:
        if not hasattr(self, "county_code_to_county_dict"):
            self.__get_counties()
        if county_code not in self.county_code_to_county_dict:
            return None
        return self.county_code_to_county_dict[county_code]

    def set_output_filepath(self, output_filepath: str):
        self.output_filepath = output_filepath

    def save_svg(self):
        if self.output_filepath is None:
            raise ValueError("output_filepath is not set")
        # create folder if necessary
        dir_name = os.path.dirname(self.output_filepath)
        os.makedirs(dir_name, exist_ok=True)
        with open(self.output_filepath, "wb") as f:
            f.write(etree.tostring(self.svg_root))
            print("Saved to " + self.output_filepath)


class CountyMapWithOutput(CountyMap):
    def __init__(self, output_filepath: str):
        super().__init__()
        self.set_output_filepath(output_filepath)
