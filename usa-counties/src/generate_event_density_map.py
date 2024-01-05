import json
from markdown_table_generator import generate_markdown, table_from_string_list, Alignment
from typing import Dict, List
from svg import CountyMap, generate_density_map, get_county_code_to_object_keys_dict

YEAR = 2024
output_prefix = f'output/event_density_map/{YEAR}'
event_key_to_county_codes_filepath = f'./output/event_locations/{YEAR}/event_key_to_county_codes.json'

# Load the event_key_to_county_codes from a file
event_key_to_county_codes: Dict[str, List[str]] = {}
with open(event_key_to_county_codes_filepath, 'r') as f:
    event_key_to_county_codes = json.load(f)

county_map = CountyMap("../assets/usa_counties.svg", f'{output_prefix}/output.svg')
county_code_to_event_keys_dict: Dict[str, List[str]] = get_county_code_to_object_keys_dict(event_key_to_county_codes)
generate_density_map(county_map, county_code_to_event_keys_dict)

# Generate markdown table
rows = []
for county_code, event_keys in county_code_to_event_keys_dict.items():
    county = county_map.get_county(county_code)
    if county is None:
        continue
    rows.append([county.get_name(), len(event_keys)])
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