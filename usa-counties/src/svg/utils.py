from .CountyMap import CountyMap
from typing import Dict, List

def get_county_code_to_object_keys_dict(object_key_to_county_codes: Dict[str, List[str]]) -> Dict[str, List[str]]:
    county_code_to_object_keys_dict: Dict[str, List[str]] = {}
    for object_key, county_codes in object_key_to_county_codes.items():
        for county_code in county_codes:
            if county_code not in county_code_to_object_keys_dict:
                county_code_to_object_keys_dict[county_code] = []
            county_code_to_object_keys_dict[county_code].append(object_key)
    return county_code_to_object_keys_dict

def generate_density_map(county_map: CountyMap, county_code_to_object_keys_dict: Dict[str, List[str]]):
    # Set all counties to white by default
    county_map.for_each_county(lambda county: county.set_fill(255, 255, 255))

    # Set the fill of each county based on the number of events in that county
    max_num_objects = max([len(object_keys) for object_keys in county_code_to_object_keys_dict.values()])
    for county_code, object_keys in county_code_to_object_keys_dict.items():
        county = county_map.get_county(county_code)
        if county is None:
            continue
        num_objects = len(object_keys)
        r = 255
        g = 255
        b = 255
        if num_objects > 0:
            r = 230 - int(230 * (num_objects / max_num_objects))
            g = 230 - int(230 * (num_objects / max_num_objects))
        county.set_fill(r, g, b)
        title = f'{county.get_title()} ({num_objects}): {", ".join(object_keys)}'
        county.set_title(title)

    county_map.save_svg()