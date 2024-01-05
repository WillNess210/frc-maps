class City:
    def __init__(self, city_name, state_name, state_code, county_code):
        self.__city_name = city_name
        self.__state_name = state_name
        self.__state_code = state_code
        self.__county_code = county_code
    
    # getters
    def get_city_name(self):
        return self.__city_name
    
    def get_state_name(self):
        return self.__state_name
    
    def get_state_code(self):
        return self.__state_code
    
    def get_county_code(self):
        return self.__county_code
    
    def __str__(self):
        return self.__city_name + ", " + self.__state_name + " (" + self.__county_code + ")"