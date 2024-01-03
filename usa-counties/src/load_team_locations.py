from location import CityDataset

us_cities_filepath = "../assets/uscities.csv"

city_dataset = CityDataset(us_cities_filepath)

gj = city_dataset.get_county_code("Grand Junction", "Colorado")
print(gj)