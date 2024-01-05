
from .LocationObject import LocationObject

class Team(LocationObject):    
    def __init__(self, tba_team):
        super().__init__(tba_team, "Team")