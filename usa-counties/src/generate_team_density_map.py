import json
from markdown_table_generator import generate_markdown, table_from_string_list, Alignment
from typing import Dict, List
from svg import CountyMap

YEAR = 2024
output_prefix = f'output/density_map/{YEAR}'
team_key_to_county_codes_filepath = f'./output/team_locations/{YEAR}/team_key_to_county_codes.json'

# Load the team_key_to_county_codes from a file
team_key_to_county_codes: Dict[str, List[str]] = {}
with open(team_key_to_county_codes_filepath, 'r') as f:
    team_key_to_county_codes = json.load(f)

county_map = CountyMap("../assets/usa_counties.svg", f'{output_prefix}/output.svg')
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
        r = 230 - int(230 * (num_teams / max_num_teams))
        g = 230 - int(230 * (num_teams / max_num_teams))
    county.set_fill(r, g, b)
    title = f'{county.get_title()} ({num_teams}): {", ".join(team_keys)}'
    county.set_title(title)

county_map.save_svg()


# Generate markdown table
rows = []
for county_code, team_keys in county_code_to_team_keys_dict.items():
    county = county_map.get_county(county_code)
    if county is None:
        continue
    rows.append([county.get_name(), len(team_keys)])
rows.sort(key=lambda row: row[1], reverse=True)

# calculate ranks
rows_with_rank = []
current_rank = 1
for i in range(len(rows)):
    i_county_count = rows[i]
    # determine if we need to prepend T to the rank
    prepend_t = False
    tied_with_previous = False
    if i > 0:
        previous_county_count = rows[i - 1][1]
        if i_county_count[1] == previous_county_count:
            prepend_t = True
            tied_with_previous = True
    else:
        next_county_count = rows[i + 1][1]
        if i_county_count[1] == next_county_count:
            prepend_t = True

    if not prepend_t and i < len(rows) - 1:
        next_county_count = rows[i + 1][1]
        if i_county_count[1] == next_county_count:
            prepend_t = True

    if not tied_with_previous:
        current_rank = i + 1
    
    i_rank = current_rank if not prepend_t else f'T{current_rank}'
    new_row = [i_rank] + rows[i]
    rows_with_rank.append(new_row)

# prepend header row
rows = [['Rank', 'County', 'Number of Teams']] + rows_with_rank
# turn every row into strings
rows = [[str(cell) for cell in row] for row in rows]

table = table_from_string_list(rows, Alignment.CENTER)
markdown = generate_markdown(table)
with open(f'{output_prefix}/output.md', 'w') as f:
    f.write(markdown)