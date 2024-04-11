import json
from location import CountyLocationDataset, CountyDistanceDataset
from svg import CountyMap, get_county_code_to_object_keys_dict, County
from typing import Dict, List
from files import OutputFileCreator

filepaths = CONFIG.get_filepaths()

starting_ownership_filepath = filepaths.get_starting_ownership_filepath()

team_key_to_county_codes_filepath = filepaths.get_team_key_to_county_codes_filepath()
active_teams_for_year_filepath = filepaths.get_team_list_filepath()
county_location_dataset_filepath = filepaths.get_county_location_dataset_filepath()
precomputed_county_distance_filepath = filepaths.get_precomputed_county_distance_filepath()

county_location_dataset = CountyLocationDataset(county_location_dataset_filepath)
county_distance_dataset = CountyDistanceDataset(precomputed_county_distance_filepath)

# Load the team_key_to_county_codes from a file
team_key_to_county_codes: Dict[str, List[str]] = {}
with open(team_key_to_county_codes_filepath, "r") as f:
    team_key_to_county_codes = json.load(f)
county_map = CountyMap()
county_code_to_team_keys_dict: Dict[str, List[str]] = (
    get_county_code_to_object_keys_dict(team_key_to_county_codes)
)

# expand into empty counties
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

# Save the updated county_code_to_team_keys_dict to a starting_ownership_filepath
output_file_creator = OutputFileCreator()
output_file_creator.json_dump(county_code_to_team_keys_dict, starting_ownership_filepath)
