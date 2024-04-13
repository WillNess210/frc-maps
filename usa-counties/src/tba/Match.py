from typing import Dict, List, Optional

RED_ALLIANCE_KEY = "red"
BLUE_ALLIANCE_KEY = "blue"


class Match:
    def __init__(self, tba_match: Dict):
        self.__actual_time: int = tba_match["actual_time"]
        self.__blue_team_keys: List[str] = tba_match["alliances"]["blue"]["team_keys"]
        self.__red_team_keys: List[str] = tba_match["alliances"]["red"]["team_keys"]
        self.__winning_alliance_key: Optional[str] = tba_match["winning_alliance"]

    def get_actual_time(self) -> int:
        return self.__actual_time

    def get_blue_team_keys(self) -> List[str]:
        return self.__blue_team_keys

    def get_red_team_keys(self) -> List[str]:
        return self.__red_team_keys

    def get_winning_alliance_key(self) -> Optional[str]:
        return self.__winning_alliance_key

    def get_losing_alliance_team_keys(self) -> Optional[List[str]]:
        if self.__winning_alliance_key == RED_ALLIANCE_KEY:
            return self.__blue_team_keys
        elif self.__winning_alliance_key == BLUE_ALLIANCE_KEY:
            return self.__red_team_keys
        return None

    def __str__(self) -> str:
        return f"Match(b={self.__blue_team_keys}, r={self.__red_team_keys}, w={self.__winning_alliance})"
