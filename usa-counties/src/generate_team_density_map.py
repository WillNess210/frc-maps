import json
from typing import Dict, List
from svg import CountyMap, generate_density_map, get_county_code_to_object_keys_dict
from rank import generate_ranked_county_table

YEAR = 2024
output_prefix = f'output/density_map/{YEAR}'
team_key_to_county_codes_filepath = f'./output/team_locations/{YEAR}/team_key_to_county_codes.json'

# Load the team_key_to_county_codes from a file
team_key_to_county_codes: Dict[str, List[str]] = {}
with open(team_key_to_county_codes_filepath, 'r') as f:
    team_key_to_county_codes = json.load(f)

county_map = CountyMap("../assets/usa_counties.svg", f'{output_prefix}/output.svg')
county_code_to_team_keys_dict: Dict[str, List[str]] = get_county_code_to_object_keys_dict(team_key_to_county_codes)
generate_density_map(county_map, county_code_to_team_keys_dict)

# Generate markdown table
markdown = generate_ranked_county_table(county_map, county_code_to_team_keys_dict, 'Team')
with open(f'{output_prefix}/output.md', 'w') as f:
    f.write(markdown)
    print(f'Saved to {output_prefix}/output.md')