# frc-maps
## Purpose
The purpose of this project is to generate geographic data visualizations for the FIRST Robotics Competition.

## Scripts
- `generate_random_colors.py`: a test script that interfaces with the County SVG code to ensure we can access each county, change its color + title
- `generate_density_map.py`: generates a county map with colors corresponding to how many teams are in that county and titles for each county with team keys (prereq: output of `load_team_locations.py`). Also generates a markdown table.
- `load_team_locations.py`: generate a JSON file with a mapping from team key -> [county codes]
- `generate_event_density_map.py`: generates a county map with colors corresponding to how many events are in that county and titles for each county with event keys (prereq: output of `load_event_locations.py`). Also generates a markdown table.
- `load_event_locations.py`: generate a JSON file with a mapping from event key -> [county codes]


## Setup
1. Create a `.env` in the `usa-counties/src` folder that matches the `.env.example` template located in the same folder.
2. As of now, you must be in the `usa-counties/src` directory to run commands (ex: `python3 ./generate_random_colors.py`)
 - Eventually I want to make this runnable from the main directory
3. TODO: add instructions on setting up conda env

## Data Sources
- In order to determine what county each team is in, we are using the following US City dataset: https://simplemaps.com/data/us-cities
- If the city dataset does not work, the backup is this zip code dataset: https://www.kaggle.com/datasets/danofer/zipcodes-county-fips-crosswalk