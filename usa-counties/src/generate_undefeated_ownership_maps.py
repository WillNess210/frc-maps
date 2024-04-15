from svg import TeamCountyMapFactory
from config import CONFIG
import json
from typing import Dict, List, Set
from svg import get_county_code_to_object_keys_dict
from location import (
    expand_teams_into_empty_counties,
)
from files import OutputFileCreator

filepaths = CONFIG.get_filepaths()
undefeated_filepaths = filepaths.get_undefeated_filepaths_in_order()
if undefeated_filepaths is None:
    raise ValueError("Ownership filepaths are None")


def get_team_key_to_county_codes() -> Dict[str, List[str]]:
    with open(filepaths.get_team_key_to_county_codes_filepath(), "r") as f:
        return json.load(f)


def filter_teams_to_keep_undefeated_only(
    team_key_to_county_codes: Dict[str, List[str]], undefeated_teams: Set[str]
) -> Dict[str, List[str]]:
    return {
        team_key: county_codes
        for team_key, county_codes in team_key_to_county_codes.items()
        if team_key in undefeated_teams
    }


def generate_undefeated_ownership_file(
    team_key_to_county_codes, undefeated_ownership_filepath
):
    county_code_to_team_keys_dict: Dict[str, List[str]] = (
        get_county_code_to_object_keys_dict(team_key_to_county_codes)
    )
    expand_teams_into_empty_counties(county_code_to_team_keys_dict)
    output_file_creator = OutputFileCreator()
    output_file_creator.json_dump(
        county_code_to_team_keys_dict, undefeated_ownership_filepath
    )


team_key_to_county_codes = get_team_key_to_county_codes()
for undefeated_filepath in undefeated_filepaths:
    undefeated_teams: Set[str] = set(
        json.loads(open(undefeated_filepath.filepath, "r").read())
    )
    team_key_to_county_codes = filter_teams_to_keep_undefeated_only(
        team_key_to_county_codes, undefeated_teams
    )
    print("Generating undefeated ownership file for week", undefeated_filepath.week)
    print("Number of undefeated teams:", len(undefeated_teams))
    print("Number of teams in team_key_to_county_codes:", len(team_key_to_county_codes))

    undefeated_ownership_filepath = filepaths.get_undefeated_ownership_filepath(
        undefeated_filepath.week
    )
    generate_undefeated_ownership_file(
        team_key_to_county_codes, undefeated_ownership_filepath
    )

    TeamCountyMapFactory(
        undefeated_ownership_filepath,
        filepaths.get_undefeated_map_filepath(undefeated_filepath.week),
    ).generate_map()
