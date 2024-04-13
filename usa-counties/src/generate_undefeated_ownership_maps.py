from svg import TeamCountyMapFactory
from config import CONFIG

filepaths = CONFIG.get_filepaths()
undefeated_ownership_filepaths = filepaths.get_undefeated_ownership_filepaths_in_order()
if undefeated_ownership_filepaths is None:
    raise ValueError("Ownership filepaths are None")

for undefeated_ownership_filepath in undefeated_ownership_filepaths:
    TeamCountyMapFactory(
        undefeated_ownership_filepath.filepath,
        filepaths.get_undefeated_map_filepath(undefeated_ownership_filepath.week),
    ).generate_map()
