from location import LocationFactory, CountyCodeFetcher
from environment import Environment
from tba import TBA, build_location_object_key_to_county_codes_dict
from files import OutputFileCreator, FilepathFactory
from typing import Dict, List

YEAR = 2024
filepaths = FilepathFactory(YEAR)

env = Environment()
TBA_KEY = env.get_tba_key()
tba = TBA(TBA_KEY, YEAR)

county_code_fetcher: CountyCodeFetcher = LocationFactory().get_county_code_fetcher()

print(f"Fetching all events from TBA for {YEAR}")
events = tba.get_events()
event_key_to_county_codes: Dict[str, List[str]] = (
    build_location_object_key_to_county_codes_dict(county_code_fetcher, events)
)

# Save the event_key_to_county_codes to a file
event_key_to_county_codes_filepath = filepaths.get_event_key_to_county_codes_filepath()
print("\nSaving event_key_to_county_codes to: " + event_key_to_county_codes_filepath)
output_file_creator = OutputFileCreator()
output_file_creator.json_dump(
    event_key_to_county_codes, event_key_to_county_codes_filepath
)
