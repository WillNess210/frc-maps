from svg import CountyMapWithOutput
from frc_colors import FrcColorDataset
from colorhash import ColorHash
import json
from typing import Dict, List
from config import CONFIG

filepaths = CONFIG.get_filepaths()

output_filepaths = filepaths.get_ownership_map_output_filepaths()
starting_ownership_filepath = filepaths.get_starting_ownership_filepath()

team_key_to_color_filepath = filepaths.get_team_key_to_frc_color_filepath()

frc_color_dataset = FrcColorDataset(team_key_to_color_filepath)
county_map = CountyMapWithOutput(output_filepaths.get_map_output())
# load starting_ownership_filepath
county_code_to_team_keys_dict: Dict[str, List[str]] = json.loads(
    open(starting_ownership_filepath).read()
)

county_map.for_each_county(lambda county: county.set_fill(255, 255, 255))
for county_code, object_keys in county_code_to_team_keys_dict.items():
    county = county_map.get_county(county_code)
    if county is None:
        continue
    num_objects = len(object_keys)
    # if county is owned by one team, set to that team's color
    if num_objects == 1:
        team_color = frc_color_dataset.get_color(object_keys[0])
        county.set_fill_color(team_color)
    elif num_objects > 1:
        color = ColorHash(",".join(object_keys)).hex
        county.set_fill_color(color)
    title = f'{county.get_title()} ({num_objects}): {", ".join(object_keys)}'
    county.set_title(title)

county_map.save_svg()
