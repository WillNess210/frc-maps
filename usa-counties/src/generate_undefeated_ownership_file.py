from config import CONFIG
from environment import Environment
from tba import TBA, Match
import json
from typing import Dict, List
from files import OutputFileCreator

YEAR = CONFIG.get_year()
filepaths = CONFIG.get_filepaths()

env = Environment()
TBA_KEY = env.get_tba_key()
tba = TBA(TBA_KEY, YEAR)

WEEK_TO_PROCESS = 6

# load starting_ownership_filepath
county_code_to_team_keys_dict: Dict[str, List[str]] = json.loads(
    open(filepaths.get_starting_ownership_filepath()).read()
)

# generate team key -> county codes dict
team_key_to_county_codes_dict: Dict[str, List[str]] = {}
for county_code, team_keys in county_code_to_team_keys_dict.items():
    for team_key in team_keys:
        if team_key not in team_key_to_county_codes_dict:
            team_key_to_county_codes_dict[team_key] = []
        team_key_to_county_codes_dict[team_key].append(county_code)

print(f"Fetching all events from TBA for {YEAR}")
events = tba.get_events()
events = list(filter(lambda event: event.get_week() <= WEEK_TO_PROCESS, events))
print(f"Found {len(events)} events to process")


def process_team_loss(team_key: str):
    if team_key not in team_key_to_county_codes_dict:
        return
    county_codes = team_key_to_county_codes_dict[team_key]
    for county_code in county_codes:
        county_code_to_team_keys_dict[county_code].remove(team_key)
    del team_key_to_county_codes_dict[team_key]


def process_match(match: Match, number_of_matches_played_by_team: Dict[str, int]):
    losing_alliance = match.get_losing_alliance_team_keys()
    for team_key in match.get_blue_team_keys() + match.get_red_team_keys():
        if team_key not in number_of_matches_played_by_team:
            process_team_loss(team_key)
            continue
        number_of_matches_played_by_team[team_key] += 1
    if losing_alliance is None:
        return
    for team_key in losing_alliance:
        process_team_loss(team_key)


def process_event(event_key: str):
    matches = tba.get_event_matches(event_key)
    teams = tba.get_event_team_keys(event_key)
    number_of_matches_played_by_team = {team: 0 for team in teams}
    # remove teams that lose a match
    for match in matches:
        process_match(match, number_of_matches_played_by_team)
    # remove teams that did not play a match at an event they were registered for
    for team, number_of_matches_played in number_of_matches_played_by_team.items():
        if number_of_matches_played > 0:
            continue
        process_team_loss(team)


for event in events:
    process_event(event.get_key())

# Save the updated county_code_to_team_keys_dict to a starting_ownership_filepath
output_file_creator = OutputFileCreator()
output_file_creator.json_dump(
    county_code_to_team_keys_dict,
    filepaths.get_undefeated_ownership_filepath(WEEK_TO_PROCESS),
)
