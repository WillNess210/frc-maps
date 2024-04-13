from svg import TeamCountyMapFactory
from config import CONFIG

filepaths = CONFIG.get_filepaths()

output_filepaths = filepaths.get_ownership_map_output_filepaths()
starting_ownership_filepath = filepaths.get_starting_ownership_filepath()

TeamCountyMapFactory(starting_ownership_filepath, output_filepaths).generate_map()
