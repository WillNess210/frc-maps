"""Fetches FRC team colors from the FRC Colors API and dumps the data to a JSON file."""

from environment import Environment
from tba import TBA
from files import OutputFileCreator
from frc_colors import FrcColors
from config import CONFIG

# script which calls endpoint multiple times then dumps the data to a JSON file
BASE_URL = "https://api.frc-colors.com/v1/team"
MAX_FRC_COLORS_PAGE_SIZE = 100
YEAR = CONFIG.get_year()
filepaths = CONFIG.get_filepaths()

env = Environment()
TBA_KEY = env.get_tba_key()
tba = TBA(TBA_KEY, YEAR)

print(f"Fetching {YEAR} teams from TBA")
tba_teams = tba.get_teams()
tba_team_numbers = [tba_team.get_key()[3:] for tba_team in tba_teams]

tba_team_colors = FrcColors().get_frc_colors(tba_team_numbers)

# dump file
output_file_creator = OutputFileCreator()
output_file_creator.json_dump(
    tba_team_colors, filepaths.get_team_key_to_frc_color_filepath()
)
