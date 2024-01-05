import json
from markdown_table_generator import generate_markdown, table_from_string_list, Alignment
from typing import Dict, List, Tuple
from svg import CountyMap, generate_density_map, get_county_code_to_object_keys_dict
from rank import calculate_rank

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
rows: List[Tuple[str, int]] = []
for county_code, team_keys in county_code_to_team_keys_dict.items():
    county = county_map.get_county(county_code)
    if county is None:
        continue
    rows.append([county.get_name(), len(team_keys)])

# calculate ranks
rows_with_rank = calculate_rank(rows, lambda row: row[1], reverse=True)
rows_with_rank = [[row.get_rank()] + row.get_data() for row in rows_with_rank]

# prepend header row
rows = [['Rank', 'County', 'Number of Teams']] + rows_with_rank
# turn every row into strings
rows = [[str(cell) for cell in row] for row in rows]

table = table_from_string_list(rows, Alignment.CENTER)
markdown = generate_markdown(table)
with open(f'{output_prefix}/output.md', 'w') as f:
    f.write(markdown)