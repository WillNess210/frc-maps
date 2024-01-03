from lxml import etree
from typing import List, Callable, Dict, Optional
from .County import County
import os

class CountyMap:
    def __init__(self, source_filepath, output_filepath):
        self.svg_root = etree.parse(source_filepath).getroot()
        self.g_root = self.svg_root[2]
        self.output_filepath = output_filepath

    def __get_counties(self):
        if hasattr(self, "counties"):
            return self.counties
        counties: List[County] = []
        county_code_to_county_dict: Dict[str, County] = {}
        for state in self.g_root:
            for county in state:
                county_obj = County(county)
                counties.append(county_obj)
                county_code_to_county_dict[county.attrib["id"][1:]] = county_obj
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

    def save_svg(self):
        # create folder if necessary
        dir_name = os.path.dirname(self.output_filepath)
        os.makedirs(dir_name, exist_ok=True)
        with open(self.output_filepath, "wb") as f:
            f.write(etree.tostring(self.svg_root))
            print("Saved to " + self.output_filepath)
