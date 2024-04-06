import json
from typing import Dict, List
from svg import CountyMap, generate_density_map, get_county_code_to_object_keys_dict
from rank import generate_ranked_county_table
from files import FilepathFactory

YEAR = 2024
filepaths = FilepathFactory(YEAR)
output_filepaths = filepaths.get_event_density_output_filepaths()
event_key_to_county_codes_filepath = filepaths.get_event_key_to_county_codes_filepath()

# Load the event_key_to_county_codes from a file
event_key_to_county_codes: Dict[str, List[str]] = {}
with open(event_key_to_county_codes_filepath, "r") as f:
    event_key_to_county_codes = json.load(f)

county_map = CountyMap(
    filepaths.get_usa_counties_svg_filepath(), output_filepaths.get_map_output()
)
county_code_to_event_keys_dict: Dict[str, List[str]] = (
    get_county_code_to_object_keys_dict(event_key_to_county_codes)
)
generate_density_map(county_map, county_code_to_event_keys_dict)

# Generate markdown table
markdown = generate_ranked_county_table(
    county_map, county_code_to_event_keys_dict, "Event"
)
with open(output_filepaths.get_table_output(), "w") as f:
    f.write(markdown)
    print(f"Saved to {output_filepaths.get_table_output()}")
