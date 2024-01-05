
from .LocationObject import LocationObject, buildLocationObjectString

class Team(LocationObject):    
    def __str__(self):
        return buildLocationObjectString(self, "Team")