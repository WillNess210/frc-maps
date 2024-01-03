import tbapy
from typing import List
from .Team import Team

class TBA:
    def __init__(self, tba_key, year):
        self.__tba = tbapy.TBA(tba_key)
        self.__year = year

    def get_teams(self) -> List[Team]:
        tba_teams = self.__tba.teams(page=0, year=self.__year)
        return [Team(tba_team) for tba_team in tba_teams]
    
