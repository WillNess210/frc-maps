import json
from typing import Dict, List
from colorhash import ColorHash
from svg import CountyMap, get_county_code_to_object_keys_dict, County
from location import CountyLocationDataset, CountyDistanceDataset
from frc_colors import FrcColorDataset


YEAR = 2024
output_prefix = f"output/team_map/{YEAR}"
team_key_to_county_codes_filepath = (
    f"./output/team_locations/{YEAR}/team_key_to_county_codes.json"
)
team_key_to_color_filepath = f"./output/frc-colors/{YEAR}/frc-colors.json"
county_location_dataset_filepath = "../assets/counties_loc.csv"
precomputed_county_distance_filepath = (
    "./output/precomputed-county-distance/precomputed-county-distance.json"
)

# Load the team_key_to_county_codes from a file
team_key_to_county_codes: Dict[str, List[str]] = {}
with open(team_key_to_county_codes_filepath, "r") as f:
    team_key_to_county_codes = json.load(f)

# Load the team_key_to_color from a file
frc_color_dataset = FrcColorDataset(team_key_to_color_filepath)

county_map = CountyMap("../assets/usa_counties.svg", f"{output_prefix}/output.svg")
county_code_to_team_keys_dict: Dict[str, List[str]] = (
    get_county_code_to_object_keys_dict(team_key_to_county_codes)
)

county_location_dataset = CountyLocationDataset(county_location_dataset_filepath)
county_distance_dataset = CountyDistanceDataset(precomputed_county_distance_filepath)

# 1. Loop through each county. Skip if county already has teams
# 2. If county is empty, determine closest county with teams and add those teams to the empty county


def process_county(county: County):
    if (
        county.get_fips() in county_code_to_team_keys_dict
        and len(county_code_to_team_keys_dict[county.get_fips()]) > 0
    ):
        return
    closest_counties = county_distance_dataset.get_closest_counties_for_county(
        county.get_fips()
    )
    for closest_county in closest_counties:
        closest_county_teams = county_code_to_team_keys_dict.get(
            closest_county.get_county_fips()
        )
        if closest_county_teams is not None and len(closest_county_teams) > 0:
            county_code_to_team_keys_dict[county.get_fips()] = closest_county_teams
            return
    print("No nearby counties with teams found for county code", county.get_fips())
    print(
        "Closest counties:",
        ",".join([f"{c.get_county_fips()}({"NA" if c.get_county_fips() not in county_code_to_team_keys_dict else len(county_code_to_team_keys_dict[c.get_fips()])})" for c in closest_counties]),
    )
    raise ValueError(
        f"No nearby counties with teams found for county code {county.get_fips()}"
    )


county_map.for_each_county(process_county)
# TODO refactor project to this structure:
# source of truth for map should be done in JSON file in format of county code -> team list, and then a python script to generate the map for the JSON


def generate_team_map(
    county_map: CountyMap,
    frc_color_dataset: FrcColorDataset,
    county_code_to_team_keys_dict: Dict[str, List[str]],
):
    """
    Generate a team map
    """

    # Set all counties to white by default
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


generate_team_map(county_map, frc_color_dataset, county_code_to_team_keys_dict)
