from location import CityDataset, ZipCodeDataset, CountyCodeFetcher
from environment import Environment
from tba import TBA
from files import OutputFileCreator
from typing import Dict, List

YEAR = 2024

env = Environment()
TBA_KEY = env.get_tba_key()
TBA = TBA(TBA_KEY, YEAR)

us_cities_filepath = "../assets/uscities.csv"
city_dataset = CityDataset(us_cities_filepath)

zipcodes_filepath = "../assets/ZIP-COUNTY-FIPS_2017-06.csv"
zipcode_dataset = ZipCodeDataset(zipcodes_filepath)

county_code_fetcher = CountyCodeFetcher(city_dataset, zipcode_dataset)

teams = TBA.get_teams()
team_key_to_county_codes: Dict[str, List[str]] = {}
for team in teams:
    if not team.is_usa_team():
        print("Skipping non-USA team: " + str(team))
        continue
    team_county_codes = county_code_fetcher.get_county_codes(team.get_city(), team.get_state(), team.get_zipcode())
    if team_county_codes is None:
        # If you are seeing this error, manually add the teams city and state to the HARDCODED_CITIES list in CityDataset.py
        # Use google to find the correct county & code
        raise Exception("Could not find county code for team: " + str(team))
    print("Found county codes for team: " + str(team) + " -> " + str(team_county_codes))
    team_key_to_county_codes[team.get_key()] = team_county_codes

# Print how many teams have mutliple county codes
number_of_teams_with_multiple_county_codes = len([team_key for team_key in team_key_to_county_codes.keys() if len(team_key_to_county_codes[team_key]) > 1])
print("\nNumber of teams with multiple county codes: " + str(number_of_teams_with_multiple_county_codes))

# Save the team_key_to_county_codes to a file
team_key_to_county_codes_filepath = f'./output/team_locations/{YEAR}/team_key_to_county_codes.json'
print("\nSaving team_key_to_county_codes to: " + team_key_to_county_codes_filepath)
output_file_creator = OutputFileCreator()
output_file_creator.json_dump(team_key_to_county_codes, team_key_to_county_codes_filepath)