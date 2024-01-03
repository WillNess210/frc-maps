from location import CityDataset
from environment import Environment
from tba import TBA

YEAR = 2024

env = Environment()
TBA_KEY = env.get_tba_key()
TBA = TBA(TBA_KEY, YEAR)

us_cities_filepath = "../assets/uscities.csv"
city_dataset = CityDataset(us_cities_filepath)
gj = city_dataset.get_county_code("Grand Junction", "Colorado")
print(gj)

teams = TBA.get_teams()
print(teams[0])