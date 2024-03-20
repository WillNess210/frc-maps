import tbapy
from typing import List
from .Team import Team
from .Event import Event

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
        return list(
            filter(
                lambda event: event.get_event_type() not in EVENT_TYPES_TO_IGNORE,
                events,
            )
        )

    def get_event_team_keys(self, event_code: str) -> List[str]:
        return self.__tba.event_teams(event_code, keys=True)
