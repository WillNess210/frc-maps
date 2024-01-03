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
# 0 teams -> (255, 255, 255) (white)
# 1 team -> (200, 200, 255) (light blue)
# in between 1 and max = linear gradient from light blue to blue
# max teams -> (0, 0, 255) (blue)
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
        r = 200 + int((num_teams / max_num_teams) * 55)
        g = 200 + int((num_teams / max_num_teams) * 55)
    county.set_fill(r, g, b)
    title = f'{county.get_title()} ({num_teams}): {", ".join(team_keys)}'
    county.set_title(title)

county_map.save_svg()
