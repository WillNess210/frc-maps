"""Dataset for FRC team colors"""

import json
from typing import Dict, Optional


class FrcColorDataset:
    """Dataset for FRC team colors"""

    def __init__(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as file:
            self.__data: Dict[str, str] = json.load(file)

    def get_color(self, team_key: str) -> Optional[str]:
        """Get the color for a team"""
        if team_key not in self.__data or self.__data[team_key] is None:
            return None
        return self.__data.get(team_key)
