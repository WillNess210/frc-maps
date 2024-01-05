USA_COUNTRY = "USA"

class Event:

    def __init__(self, tba_event):
        self.__city = tba_event.city
        self.__country = tba_event.country
        self.__key = tba_event.key
        self.__state = tba_event.state_prov
        self.__zipcode = tba_event.postal_code
        self.__event_type = tba_event.event_type_string

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
    
    def get_event_type(self):
        return self.__event_type
    
    def is_usa_event(self):
        return self.__country == USA_COUNTRY
    
    def __str__(self):
        return self.__key + " Event(" + self.__city + ", " + self.__state + ", " + str(self.__zipcode) + ", " + self.__country + ")"