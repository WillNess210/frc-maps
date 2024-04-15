from config import CONFIG
import json
from typing import Set, Optional

filepaths = CONFIG.get_filepaths()


class ActiveTeamsFactory:
    def __init__(self):
        self.__active_teams: Optional[Set[str]] = None

    def get_active_teams(self) -> Set[str]:
        if self.__active_teams is None:
            self.__active_teams = self.__load_active_teams()
        return self.__active_teams

    def __load_active_teams(self) -> Set[str]:
        active_teams: Set[str] = set()
        with open(filepaths.get_team_list_filepath(), "r") as f:
            active_teams = set(json.load(f))
        return active_teams
