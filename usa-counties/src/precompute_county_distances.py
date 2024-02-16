"""Generate a file that contains the distance between each pair of counties in the USA."""

from location import CountyLocationDataset, CountyPair
from files import OutputFileCreator
from typing import Dict


county_location_dataset_filepath = "../assets/counties_loc.csv"

county_location_dataset = CountyLocationDataset(county_location_dataset_filepath)

all_county_keys = county_location_dataset.get_county_keys()
number_of_counties = len(all_county_keys)

county_code_to_distances: Dict[str, Dict] = {}
for county_code in all_county_keys:
    county_code_to_distances[county_code] = []

for i in range(number_of_counties):
    county_one = county_location_dataset.get_county_location(all_county_keys[i])
    for j in range(i + 1, number_of_counties):
        if i == j:
            continue
        county_two = county_location_dataset.get_county_location(all_county_keys[j])
        county_distance = CountyPair(county_one, county_two).get_distance()
        county_one_distance_json = [county_one.get_county_fips(), county_distance]
        county_two_distance_json = [county_two.get_county_fips(), county_distance]
        county_code_to_distances[county_one.get_county_fips()].append(
            county_two_distance_json
        )
        county_code_to_distances[county_two.get_county_fips()].append(
            county_one_distance_json
        )
    # sort by distance ascending
    county_code_to_distances[county_one.get_county_fips()].sort(key=lambda x: x[1])

output_file_creator = OutputFileCreator()
output_file_creator.json_dump(
    county_code_to_distances,
    "output/precomputed-county-distance/precomputed-county-distance.json",
)
