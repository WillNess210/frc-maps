import pandas as pd
from .City import City
from typing import Dict, Tuple, List, Optional

# only keeping a subset of the columns to save memory
CITY_NAME_COLUMN = 'city'
STATE_NAME_COLUMN = 'state_name'
COUNTY_CODE_COLUMN = 'county_fips'
columns: List[str] = [CITY_NAME_COLUMN, STATE_NAME_COLUMN, COUNTY_CODE_COLUMN]


# some teams have no zip code, and the city is not in the city dataset, so we have to hardcode some of these :(
# copilot generated most of these because I was too lazy to look up the county codes myself, so hopefully they are correct
HARDCODED_CITIES: List[City] = [
    # city, state, county code
    City("Walpole", "Massachusetts", "25021"),
    City("Medford", "Massachusetts", "25017"),
    City("Medford", "New Jersey", "34005"),
    City("Woodbine", "Maryland", "24013"),
    City("Erie", "Michigan", "26059"),
    City("Sutton", "Massachusetts", "25027"),
    City("Wellesley Hills", "Massachusetts", "25021"),
    City("Devils Lake", "North Dakota", "38019"),
    City("Denville", "New Jersey", "34027"),
    City("Lexington", "Massachusetts", "25017"),
    City("Scituate", "Massachusetts", "25023"),
    City("Dunbarton", "New Hampshire", "33013"),
    City("Palmer", "Massachusetts", "25013"),
    City("Toms River", "New Jersey", "34029"),
    City("Saint Louis", "Missouri", "29510"),
    City("Bedford", "New Hampshire", "33011"),
    City("Ijamsville", "Maryland", "24031"),
    City("Fuquay Varina", "North Carolina", "37183"),
    City("Ozone Park", "New York", "36081"),
    City("Wayne", "New Jersey", "34031"),
    City("Saint Johns", "Florida", "12109"),
    City("JACKSON JUNCTION", "Iowa", "19019"),
    City("Del Valle", "Texas", "48453"),
    City("Coeur D Alene", "Idaho", "16055"),
    City("Wilton", "Maine", "23017"),
    City("Kents Hill", "Maine", "23017"),
    City("Hanover", "Maryland", "24003"),
    City("Pleasant Valley", "Iowa", "19163"),
    City("Wynnewood", "Pennsylvania", "42045"),
    City("Stowe", "Vermont", "50015"),
    City("New Boston", "Michigan", "26163"),
    City("Coventry", "Rhode Island", "44003"),
    City("Arden", "North Carolina", "37121"),
    City("Rosemary Beach", "Florida", "12059"),
    City("West Newbury", "Massachusetts", "25009"),
    City("Kingwood", "Texas", "48201"),
    City("Clinton Township", "Michigan", "26099"),
    City("Bark River", "Michigan", "26041"),
    City("Covert", "Michigan", "26021"),
    City("Winston Salem", "North Carolina", "37169"),
    City("Montezuma", "New Mexico", "35045"),
    City("Christchurch", "Virginia", "51036"),
    City("Southampton", "New York", "36103"),
    City("Saint Augustine", "Florida", "12109"),
    City("Chesterfield", "Virginia", "51041"),
    City("Warwick", "New York", "36111"),
    City("Saint Petersburg", "Florida", "12103"),
    City("Redford", "Michigan", "26125"),
    City("Needham", "Massachusetts", "25021"),
    City("Kennebunk", "Maine", "23031"),
    City("Vestaburg", "Michigan", "26117"),
    City("Jerome", "Michigan", "26059"),
    City("Winnetka", "California", "06037")
]

class CityDataset:
    def __init__(self, filepath):
        df = pd.read_csv(filepath, usecols=columns, dtype=str)
        self.__create_lookup_map(df)
        
    def __create_lookup_map(self, df: pd.DataFrame):
        # create a map from ("city", "state_name") to City
        self.__lookup_map: Dict[Tuple[str, str], City] = {}
        
        for city in HARDCODED_CITIES:
            key = (city.get_city_name(), city.get_state_name())
            self.__lookup_map[key] = city

        for _, row in df.iterrows():
            city_name: str = row[CITY_NAME_COLUMN]
            state_name: str = row[STATE_NAME_COLUMN]
            county_code: str = row[COUNTY_CODE_COLUMN]

            key: Tuple[str, str] = (city_name, state_name)
            city = City(city_name, state_name, county_code)
            self.__lookup_map[key] = city

    def get_city(self, city_name: str, state_name: str) -> Optional[City]:
        key = (city_name, state_name)
        if key in self.__lookup_map:
            return self.__lookup_map[key]
        return None
