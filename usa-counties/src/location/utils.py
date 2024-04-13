from svg import CountyMap, County
from config import CONFIG
from .CountyDistanceDataset import CountyDistanceDataset
from typing import Dict, List

filepaths = CONFIG.get_filepaths()
county_distance_dataset = CountyDistanceDataset(filepaths.get_precomputed_county_distance_filepath())

def process_county(county_code_to_team_keys_dict: Dict[str, List[str]], county: County):
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


def expand_teams_into_empty_counties(
        county_code_to_team_keys_dict: Dict[str, List[str]]
):
    county_map = CountyMap()
    county_map.for_each_county(lambda county: process_county(county_code_to_team_keys_dict, county))
