from tba import TBA
from files import OutputFileCreator
from typing import Set
from environment import Environment
from config import CONFIG

YEAR = CONFIG.get_year()
filepaths = CONFIG.get_filepaths()

env = Environment()
TBA_KEY = env.get_tba_key()
tba = TBA(TBA_KEY, YEAR)

events = tba.get_events()
# create set of team keys
team_keys: Set[str] = set()
for event in events:
    event_team_keys = tba.get_event_team_keys(event.get_key())
    team_keys.update(event_team_keys)
team_keys = list(sorted(team_keys))

output_file_creator = OutputFileCreator()
output_file_creator.json_dump(team_keys, filepaths.get_team_list_filepath())
