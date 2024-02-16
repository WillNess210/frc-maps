"""Dataset for FRC team colors"""

import json
from typing import Dict
from colorhash import ColorHash


class FrcColorDataset:
    """Dataset for FRC team colors"""

    def __init__(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as file:
            self.__data: Dict[str, str] = json.load(file)

    def get_color(self, team_key: str) -> str:
        """Get the color for a team"""
        if team_key not in self.__data or self.__data[team_key] is None:
            return ColorHash(team_key).hex
        return self.__data.get(team_key)
