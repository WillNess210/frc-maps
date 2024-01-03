import json
from typing import Dict, List
from svg import CountyMap

YEAR = 2024
team_key_to_county_codes_filepath = f'./output/team_locations/{YEAR}/team_key_to_county_codes.json'

# Load the team_key_to_county_codes from a file
team_key_to_county_codes: Dict[str, List[str]] = {}
with open(team_key_to_county_codes_filepath, 'r') as f:
    team_key_to_county_codes = json.load(f)

county_map = CountyMap("../assets/usa_counties.svg", f'output/density_map/{YEAR}/output.svg')
county_code_to_team_keys_dict: Dict[str, List[str]] = {}
for team_key, county_codes in team_key_to_county_codes.items():
    for county_code in county_codes:
        county = county_map.get_county(county_code)
        if county is None:
            print(f"Could not find county with code {county_code}")
            continue
        if county_code not in county_code_to_team_keys_dict:
            county_code_to_team_keys_dict[county_code] = []
        county_code_to_team_keys_dict[county_code].append(team_key)


# Set all counties to white by default
county_map.for_each_county(lambda county: county.set_fill(255, 255, 255))
# Set the fill of each county based on the number of teams in that county
# 0 teams -> white
# in between 0 and max = linear gradient from white to blue
# max teams -> blue
max_num_teams = max([len(team_keys) for team_keys in county_code_to_team_keys_dict.values()])
for county_code, team_keys in county_code_to_team_keys_dict.items():
    county = county_map.get_county(county_code)
    if county is None:
        continue
    num_teams = len(team_keys)
    r = 255
    g = 255
    b = 255
    if num_teams > 0:
        r = int(255 * (1 - num_teams / max_num_teams))
        g = int(255 * (1 - num_teams / max_num_teams))
        b = 255
    county.set_fill(r, g, b)
    title = county.get_title() + ": " + str(team_keys)

county_map.save_svg()
