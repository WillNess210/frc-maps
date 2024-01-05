from .LocationObject import LocationObject

class Event(LocationObject):
    def __init__(self, tba_event):
        self.__event_type = tba_event.event_type_string
        super().__init__(tba_event, "Event")

    def get_event_type(self)  -> str:
        return self.__event_type