from .LocationObject import LocationObject
from location import CountyCodeFetcher
from svg import CountyMap
from typing import Dict, List
from config import CONFIG

filepaths = CONFIG.get_filepaths()


def build_location_object_key_to_county_codes_dict(
    county_code_fetcher: CountyCodeFetcher, location_objects: List[LocationObject]
) -> Dict[str, List[str]]:
    not_found_location_objects = []
    location_object_key_to_county_codes: Dict[str, List[str]] = (
        __build_initial_dictionary(
            county_code_fetcher, location_objects, not_found_location_objects
        )
    )

    __print_number_of_location_objects_with_multiple_county_codes(
        location_objects, location_object_key_to_county_codes
    )
    __verify_all_location_objects_have_county_codes(
        location_objects, not_found_location_objects
    )
    __verify_every_teams_county_codes_are_in_county_map(
        location_object_key_to_county_codes
    )

    return location_object_key_to_county_codes


def __verify_every_teams_county_codes_are_in_county_map(
    location_object_key_to_county_codes,
):
    county_map = county_map = CountyMap()
    invalid_county_codes = []
    for (
        location_object_key,
        county_codes,
    ) in location_object_key_to_county_codes.items():
        for county_code in county_codes:
            county = county_map.get_county(county_code)
            if county is None:
                invalid_county_codes.append(county_code)

    invalid_county_codes = list(set(invalid_county_codes))
    if len(invalid_county_codes) > 0:
        raise Exception("Invalid county codes found: " + str(invalid_county_codes))


def __verify_all_location_objects_have_county_codes(
    location_objects, not_found_location_objects
):
    if len(not_found_location_objects) > 0:
        # If you are seeing this error, manually add the location_objects city and state to the HARDCODED_CITIES list in CityDataset.py
        # Use google to find the correct county & code
        print(
            f"\nCould not find county code for {len(not_found_location_objects)}/{len(location_objects)} {location_objects[0].get_object_type()}s: "
        )
        for location_object in not_found_location_objects:
            print(location_object)
        raise Exception("Could not find county code for location_objects.")


def __print_number_of_location_objects_with_multiple_county_codes(
    location_objects, location_object_key_to_county_codes
):
    number_of_location_objects_with_multiple_county_codes = len(
        [
            location_object_key
            for location_object_key in location_object_key_to_county_codes.keys()
            if len(location_object_key_to_county_codes[location_object_key]) > 1
        ]
    )
    print(
        f"\nNumber of {location_objects[0].get_object_type()} with multiple county codes: "
        + str(number_of_location_objects_with_multiple_county_codes)
    )


def __build_initial_dictionary(
    county_code_fetcher, location_objects, not_found_location_objects
) -> Dict[str, List[str]]:
    location_object_key_to_county_codes: Dict[str, List[str]] = {}
    for location_object in location_objects:
        if not location_object.is_in_usa():
            print(
                f"Skipping non-USA {location_object.get_object_type()}: "
                + str(location_object)
            )
            continue
        location_object_county_codes = county_code_fetcher.get_county_codes(
            location_object.get_city(),
            location_object.get_state(),
            location_object.get_zipcode(),
        )
        if location_object_county_codes is None:
            not_found_location_objects.append(location_object)
            continue
        print(
            f"Found county codes for {location_object.get_object_type()}: "
            + str(location_object)
            + " -> "
            + str(location_object_county_codes)
        )
        location_object_key_to_county_codes[location_object.get_key()] = (
            location_object_county_codes
        )
    return location_object_key_to_county_codes
