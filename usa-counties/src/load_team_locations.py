from location import CityDataset, ZipCodeDataset, CountyCodeFetcher
from environment import Environment
from tba import TBA

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
for team in teams:
    if not team.is_usa_team():
        print("Skipping non-USA team: " + str(team))
        continue
    team_county_codes = county_code_fetcher.get_county_codes(team.get_city(), team.get_state(), team.get_zipcode())
    if team_county_codes is None:
        raise Exception("Could not find county code for team: " + str(team))
    print("Found county codes for team: " + str(team) + " -> " + str(team_county_codes))