from svg import CountyMap
from random import randint
from config import CONFIG

# create a CountyMap object
county_map = CountyMap(
    CONFIG.get_filepaths().get_usa_counties_svg_filepath(),
    "output/random_colors/output.svg",
)

# set the fill of each county to a random color
county_map.for_each_county(
    lambda county: county.set_fill(randint(0, 255), randint(0, 255), randint(0, 255))
)

# save the svg
county_map.save_svg()
