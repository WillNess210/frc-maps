from location import LocationFactory, CountyCodeFetcher
from svg import CountyMap
from environment import Environment
from tba import TBA
from files import OutputFileCreator
from typing import Dict, List

YEAR = 2024

env = Environment()
TBA_KEY = env.get_tba_key()
TBA = TBA(TBA_KEY, YEAR)

county_code_fetcher: CountyCodeFetcher = LocationFactory().get_county_code_fetcher()

print(f'Fetching all events from TBA for {YEAR}')
events = TBA.get_events()
not_found_events = []
event_key_to_county_codes: Dict[str, List[str]] = {}
for event in events:
    if not event.is_in_usa():
        print("Skipping non-USA event: " + str(event))
        continue
    event_county_codes = county_code_fetcher.get_county_codes(event.get_city(), event.get_state(), event.get_zipcode())
    if event_county_codes is None:
        not_found_events.append(event)
        continue
    print("Found county codes for event: " + str(event) + " -> " + str(event_county_codes))
    event_key_to_county_codes[event.get_key()] = event_county_codes

# Print how many events have mutliple county codes
number_of_events_with_multiple_county_codes = len([event_key for event_key in event_key_to_county_codes.keys() if len(event_key_to_county_codes[event_key]) > 1])
print("\nNumber of events with multiple county codes: " + str(number_of_events_with_multiple_county_codes))

# Throw errors if we were not able to resolve an event to a county code
if len(not_found_events) > 0:
    # If you are seeing this error, manually add the events city and state to the HARDCODED_CITIES list in CityDataset.py
    # Use google to find the correct county & code
    print(f'\nCould not find county code for {len(not_found_events)}/{len(events)} events: ')
    for event in not_found_events:
        print(event)
    raise Exception("Could not find county code for events.")
    


# Throw errors if events county code is not in the County Map
county_map = county_map = CountyMap("../assets/usa_counties.svg", "if_this_file_exists_something_went_wrong.svg")
invalid_county_codes = []
for event_key, county_codes in event_key_to_county_codes.items():
    for county_code in county_codes:
        county = county_map.get_county(county_code)
        if county is None:
            invalid_county_codes.append(county_code)

invalid_county_codes = list(set(invalid_county_codes))
if len(invalid_county_codes) > 0:
    raise Exception("Invalid county codes found: " + str(invalid_county_codes))

# Save the event_key_to_county_codes to a file
event_key_to_county_codes_filepath = f'./output/event_locations/{YEAR}/event_key_to_county_codes.json'
print("\nSaving event_key_to_county_codes to: " + event_key_to_county_codes_filepath)
output_file_creator = OutputFileCreator()
output_file_creator.json_dump(event_key_to_county_codes, event_key_to_county_codes_filepath)