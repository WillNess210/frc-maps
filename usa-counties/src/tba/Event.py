from .LocationObject import LocationObject, buildLocationObjectString

class Event(LocationObject):

    def __init__(self, tba_event):
        self.__event_type = tba_event.event_type_string
        super().__init__(tba_event)

    def get_event_type(self):
        return self.__event_type

    def __str__(self):
        return buildLocationObjectString(self, "Event")