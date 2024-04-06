from location import LocationFactory, CountyCodeFetcher
from environment import Environment
from tba import TBA, build_location_object_key_to_county_codes_dict
from files import OutputFileCreator
from typing import Dict, List
from config import CONFIG

YEAR = CONFIG.get_year()
filepaths = CONFIG.get_filepaths()

env = Environment()
TBA_KEY = env.get_tba_key()
tba = TBA(TBA_KEY, YEAR)

county_code_fetcher: CountyCodeFetcher = LocationFactory().get_county_code_fetcher()

print(f"Fetching all teams from TBA for {YEAR}")
teams = tba.get_teams()
team_key_to_county_codes: Dict[str, List[str]] = (
    build_location_object_key_to_county_codes_dict(county_code_fetcher, teams)
)

# Save the team_key_to_county_codes to a file
team_key_to_county_codes_filepath = filepaths.get_team_key_to_county_codes_filepath()
print("\nSaving team_key_to_county_codes to: " + team_key_to_county_codes_filepath)
output_file_creator = OutputFileCreator()
output_file_creator.json_dump(
    team_key_to_county_codes, team_key_to_county_codes_filepath
)
