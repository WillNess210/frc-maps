from files import FilepathFactory

filepaths = FilepathFactory(2020)
print(filepaths.get_county_location_dataset_filepath())
