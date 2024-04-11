from svg import CountyMap, County
from location import CountyLocationDataset
from config import CONFIG

filepaths = CONFIG.get_filepaths()

county_map = CountyMap()

county_location_dataset = CountyLocationDataset(
    filepaths.get_county_location_dataset_filepath()
)

num_counties_missing = 0


def process_county(county: County):
    global num_counties_missing  # Declare the variable as global
    fips = county.get_fips()
    if county_location_dataset.get_county_location(fips) is None:
        num_counties_missing = num_counties_missing + 1


county_map.for_each_county(process_county)
print(f"Number of missing counties: {num_counties_missing}")
