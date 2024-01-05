USA_COUNTRY = "USA"

# common class for TBA response types that have a location
class LocationObject:
    def __init__(self, tba_team, object_type: str):
        self.__city = tba_team.city
        self.__country = tba_team.country
        self.__key = tba_team.key
        self.__state = tba_team.state_prov
        self.__zipcode = tba_team.postal_code

        self.__object_type = object_type

    def get_city(self) -> str:
        return self.__city
    
    def get_country(self) -> str:
        return self.__country
    
    def get_key(self) -> str:
        return self.__key
    
    def get_state(self) -> str:
        return self.__state
    
    def get_zipcode(self) -> str:
        return self.__zipcode
    
    def get_object_type(self) -> str:
        return self.__object_type
    
    def is_in_usa(self) -> bool:
        return self.__country == USA_COUNTRY
    
    def __str__(self) -> str:
        return f'{self.__object_type}({self.__key})({self.__city}, {self.__state}, {self.__zipcode}, {self.__country})'