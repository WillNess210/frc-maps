from svg import CountyMapWithOutput
from random import randint

# create a CountyMap object
county_map = CountyMapWithOutput(
    "output/random_colors/output.svg",
)

# set the fill of each county to a random color
county_map.for_each_county(
    lambda county: county.set_fill(randint(0, 255), randint(0, 255), randint(0, 255))
)

# save the svg
county_map.save_svg()
