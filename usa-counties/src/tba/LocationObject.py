USA_COUNTRY = "USA"

# common class for TBA response types that have a location
class LocationObject:
    def __init__(self, tba_team):
        self.__city = tba_team.city
        self.__country = tba_team.country
        self.__key = tba_team.key
        self.__state = tba_team.state_prov
        self.__zipcode = tba_team.postal_code

    def get_city(self):
        return self.__city
    
    def get_country(self):
        return self.__country
    
    def get_key(self):
        return self.__key
    
    def get_state(self):
        return self.__state
    
    def get_zipcode(self):
        return self.__zipcode
    
    def is_in_usa(self):
        return self.__country == USA_COUNTRY
    
    def __str__(self):
        return buildLocationObjectString("LocationObject")
    
def buildLocationObjectString(locationObject: LocationObject, object_type: str) -> str:
    return f'{locationObject.get_key()} {object_type}({locationObject.get_city()}, {locationObject.get_state()}, {locationObject.get_zipcode()}, {locationObject.get_country()})'