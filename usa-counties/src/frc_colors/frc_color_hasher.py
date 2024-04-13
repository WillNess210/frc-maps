from . import FrcColorDataset
from colorhash import ColorHash
from config import CONFIG
from typing import List

filepaths = CONFIG.get_filepaths()


class FrcColorHasher:
    def __init__(self):
        self.__frc_color_dataset = FrcColorDataset(
            filepaths.get_team_key_to_frc_color_filepath()
        )

    def get_color_for_team(self, team_key: str) -> str:
        dataset_color = self.__frc_color_dataset.get_color(team_key)
        if dataset_color is not None:
            return dataset_color
        return ColorHash(team_key).hex

    def get_color_for_teams(self, team_keys: List[str]) -> str:
        if len(team_keys) == 0:
            return "#ffffff"
        if len(team_keys) == 1:
            return self.get_color_for_team(team_keys[0])
        return ColorHash(",".join(team_keys)).hex
