import json
from typing import Dict, List
from svg import CountyMap

YEAR = 2024
output_prefix = f'output/event_density_map/{YEAR}'
event_key_to_county_codes_filepath = f'./output/event_locations/{YEAR}/event_key_to_county_codes.json'

# Load the event_key_to_county_codes from a file
event_key_to_county_codes: Dict[str, List[str]] = {}
with open(event_key_to_county_codes_filepath, 'r') as f:
    event_key_to_county_codes = json.load(f)

county_map = CountyMap("../assets/usa_counties.svg", f'{output_prefix}/output.svg')
county_code_to_event_keys_dict: Dict[str, List[str]] = {}
for event_key, county_codes in event_key_to_county_codes.items():
    for county_code in county_codes:
        county = county_map.get_county(county_code)
        if county is None:
            print(f"Could not find county with code {county_code}")
            continue
        if county_code not in county_code_to_event_keys_dict:
            county_code_to_event_keys_dict[county_code] = []
        county_code_to_event_keys_dict[county_code].append(event_key)


# Set all counties to white by default
county_map.for_each_county(lambda county: county.set_fill(255, 255, 255))

# Set the fill of each county based on the number of events in that county
max_num_events = max([len(event_keys) for event_keys in county_code_to_event_keys_dict.values()])
for county_code, event_keys in county_code_to_event_keys_dict.items():
    county = county_map.get_county(county_code)
    if county is None:
        continue
    num_events = len(event_keys)
    r = 255
    g = 255
    b = 255
    if num_events > 0:
        r = 230 - int(230 * (num_events / max_num_events))
        g = 230 - int(230 * (num_events / max_num_events))
    county.set_fill(r, g, b)
    title = f'{county.get_title()} ({num_events}): {", ".join(event_keys)}'
    county.set_title(title)

county_map.save_svg()