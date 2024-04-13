from .LocationObject import LocationObject

MANUAL_WEEK_DEFINITIONS = {
    2024: {
        1: {
            "final_starting_date": "2024-03-03",
        },
        2: {
            "final_starting_date": "2024-03-08",
        },
        3: {
            "final_starting_date": "2024-03-15",
        },
        4: {
            "final_starting_date": "2024-03-22",
        },
        5: {
            "final_starting_date": "2024-03-29",
        },
        6: {
            "final_starting_date": "2024-04-05",
        },
        7: {
            "final_starting_date": "2024-04-30",
        },
    }
}


class Event(LocationObject):
    def __init__(self, tba_event):
        self.__event_type = tba_event.event_type_string
        self.__start_date = tba_event.start_date
        self.__end_date = tba_event.end_date
        self.__year = tba_event.year
        super().__init__(tba_event, "Event")

    def get_event_type(self) -> str:
        return self.__event_type

    def get_start_date(self) -> str:
        return self.__start_date

    def get_end_date(self) -> str:
        return self.__end_date

    def get_week(self) -> int:
        if self.__year not in MANUAL_WEEK_DEFINITIONS:
            raise ValueError(f"No manual week definitions for year {self.__year}")
        for week, week_definition in MANUAL_WEEK_DEFINITIONS[self.__year].items():
            if self.__start_date <= week_definition["final_starting_date"]:
                return week
        raise ValueError(f"No week found for event {self.get_key()}")
