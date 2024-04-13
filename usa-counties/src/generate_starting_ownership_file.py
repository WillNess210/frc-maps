import json
from location import (
    expand_teams_into_empty_counties,
)
from svg import get_county_code_to_object_keys_dict
from typing import Dict, List, Set
from files import OutputFileCreator
from config import CONFIG

filepaths = CONFIG.get_filepaths()

starting_ownership_filepath = filepaths.get_starting_ownership_filepath()

team_key_to_county_codes_filepath = filepaths.get_team_key_to_county_codes_filepath()
active_teams_for_year_filepath = filepaths.get_team_list_filepath()


# get active teams
active_teams: Set[str] = set()
with open(active_teams_for_year_filepath, "r") as f:
    active_teams = set(json.load(f))

# Load the team_key_to_county_codes from a file
# and filter out inactive teams
team_key_to_county_codes: Dict[str, List[str]] = {}
with open(team_key_to_county_codes_filepath, "r") as f:
    team_key_to_county_codes = json.load(f)
    team_key_to_county_codes = {
        team_key: county_codes
        for team_key, county_codes in team_key_to_county_codes.items()
        if team_key in active_teams
    }

county_code_to_team_keys_dict: Dict[str, List[str]] = (
    get_county_code_to_object_keys_dict(team_key_to_county_codes)
)

expand_teams_into_empty_counties(county_code_to_team_keys_dict)

# Save the updated county_code_to_team_keys_dict to a starting_ownership_filepath
output_file_creator = OutputFileCreator()
output_file_creator.json_dump(
    county_code_to_team_keys_dict, starting_ownership_filepath
)
