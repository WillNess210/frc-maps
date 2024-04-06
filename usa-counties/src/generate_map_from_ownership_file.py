from svg import CountyMap, generate_density_map
from frc_colors import FrcColorDataset
from colorhash import ColorHash
import json
from typing import Dict, List


YEAR = 2024
starting_ownership_filepath = (
    f"./output/starting_ownership/{YEAR}/starting_ownership.json"
)
output_prefix = f"output/ownership_map/{YEAR}"
team_key_to_color_filepath = f"./output/frc-colors/{YEAR}/frc-colors.json"


frc_color_dataset = FrcColorDataset(team_key_to_color_filepath)
county_map = CountyMap("../assets/usa_counties.svg", f"{output_prefix}/output.svg")
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
