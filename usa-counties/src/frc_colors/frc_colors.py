"""This module interfaces with the frc-colors API to get the primary colors of FRC teams."""

from typing import List, Dict
import requests


class FrcColors:
    """Class interfaces with the frc-colors API to get the primary colors of FRC teams."""

    def __init__(self):
        self.__base_url = "https://api.frc-colors.com/v1/team"
        self.__max_page_size = 100

    def get_frc_colors(self, team_numbers: List[str]) -> Dict[str, str]:
        """Fetches FRC team colors from the FRC Colors API
        and returns a dictionary of team numbers to primary colors."""
        team_colors = {}
        for i in range(0, len(team_numbers), self.__max_page_size):
            team_numbers_batch = team_numbers[i : i + self.__max_page_size]
            full_url = self.__base_url + "?team=" + "&team=".join(team_numbers_batch)
            response = requests.get(full_url, timeout=5).json()
            for team in response["teams"]:
                team_key = "frc" + team
                team_obj = response["teams"][team]
                if "colors" in team_obj and team_obj["colors"] is not None:
                    team_colors[team_key] = team_obj["colors"]["primaryHex"]
                else:
                    team_colors[team_key] = None
        return team_colors
