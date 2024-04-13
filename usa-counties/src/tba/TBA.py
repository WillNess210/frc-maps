import tbapy
from typing import List
from .Team import Team
from .Event import Event
from .Match import Match

EVENT_TYPES_TO_IGNORE = ["Offseason", "Preseason", "Remote", "--"]


class TBA:
    def __init__(self, tba_key, year):
        self.__tba = tbapy.TBA(tba_key)
        self.__year = year

    def get_teams(self) -> List[Team]:
        tba_teams = self.__tba.teams(year=self.__year)
        return [Team(tba_team) for tba_team in tba_teams]

    def get_events(self) -> List[Event]:
        tba_events = self.__tba.events(year=self.__year)
        events = [Event(tba_event) for tba_event in tba_events]
        events = filter(
            lambda event: event.get_event_type() not in EVENT_TYPES_TO_IGNORE, events
        )
        events = sorted(events, key=lambda event: event.get_end_date())
        return events

    def get_event_team_keys(self, event_code: str) -> List[str]:
        return self.__tba.event_teams(event_code, keys=True)

    def get_event_matches(self, event_code: str) -> List[Match]:
        tba_matches = self.__tba.event_matches(event_code, simple=True)
        return [Match(tba_match) for tba_match in tba_matches]
