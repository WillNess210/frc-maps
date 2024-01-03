
USA_COUNTRY = "USA"

class Team:
    def __init__(self, tba_team):
        self.__city = tba_team.city
        self.__country = tba_team.country
        self.__key = tba_team.key
        self.__state = tba_team.state_prov

    def get_city(self):
        return self.__city
    
    def get_country(self):
        return self.__country
    
    def get_key(self):
        return self.__key
    
    def get_state(self):
        return self.__state
    
    def is_usa_team(self):
        return self.__country == USA_COUNTRY
    
    def __str__(self):
        return f"Team(key={self.__key}, city={self.__city}, state={self.__state}, country={self.__country})"
