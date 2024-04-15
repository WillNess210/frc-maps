from config import CONFIG
from environment import Environment
from tba import TBA, Match
from typing import Dict, Set
from files import OutputFileCreator
import json

YEAR = CONFIG.get_year()
filepaths = CONFIG.get_filepaths()

WEEK_TO_PROCESS = 6

latest_undefeated_filepath_with_week = filepaths.get_latest_undefeated_filepath()

if (
    latest_undefeated_filepath_with_week is not None
    and latest_undefeated_filepath_with_week.week >= WEEK_TO_PROCESS
):
    print("The latest undefeated file is up to date")
    exit()

WEEK_TO_START_PROCESSING_AFTER = (
    latest_undefeated_filepath_with_week.week
    if latest_undefeated_filepath_with_week is not None
    else 0
)

remaining_teams_filepath: str = (
    filepaths.get_undefeated_filepath(WEEK_TO_START_PROCESSING_AFTER)
    if WEEK_TO_START_PROCESSING_AFTER > 0
    else filepaths.get_team_list_filepath()
)
remaining_teams: Set[str] = set(json.loads(open(remaining_teams_filepath, "r").read()))

# only keep undefeated teams
print(f"Fetching all events from TBA for {YEAR}")
env = Environment()
TBA_KEY = env.get_tba_key()
tba = TBA(TBA_KEY, YEAR)
events = tba.get_events()
events = list(
    filter(
        lambda event: event.get_week() > WEEK_TO_START_PROCESSING_AFTER
        and event.get_week() <= WEEK_TO_PROCESS,
        events,
    )
)
print(f"Found {len(events)} events to process")


def process_team_loss(team_key: str):
    if team_key not in remaining_teams:
        return
    remaining_teams.remove(team_key)


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
    list(remaining_teams),
    filepaths.get_undefeated_filepath(WEEK_TO_PROCESS),
)
