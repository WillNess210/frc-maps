from .CountyMap import CountyMapWithOutput
from frc_colors import FrcColorHasher
from files import MapAndTableOutputFilepaths
import json
from typing import Dict, List


class TeamCountyMapFactory:
    def __init__(
        self, ownership_filepath: str, output_filepaths: MapAndTableOutputFilepaths
    ):
        self.__ownership_filepath = ownership_filepath
        self.__output_filepaths = output_filepaths

    def generate_map(self):
        frc_color_hasher = FrcColorHasher()
        county_map = CountyMapWithOutput(self.__output_filepaths.get_map_output())
        # load ownership_filepath
        county_code_to_team_keys_dict: Dict[str, List[str]] = json.loads(
            open(self.__ownership_filepath).read()
        )

        county_map.for_each_county(lambda county: county.set_fill(255, 255, 255))
        for county_code, object_keys in county_code_to_team_keys_dict.items():
            county = county_map.get_county(county_code)
            if county is None:
                continue
            # if county is owned by one team, set to that team's color
            county_color = frc_color_hasher.get_color_for_teams(object_keys)
            county.set_fill_color(county_color)
            title = (
                f'{county.get_title()} ({len(object_keys)}): {", ".join(object_keys)}'
            )
            county.set_title(title)

        county_map.save_svg()
