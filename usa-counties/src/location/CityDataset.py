import pandas as pd
from .City import City
from typing import Dict, Tuple, List, Optional

# only keeping a subset of the columns to save memory
CITY_NAME_COLUMN = 'city'
STATE_NAME_COLUMN = 'state_name'
STATE_CODE_COLUMN = 'state_id'
COUNTY_CODE_COLUMN = 'county_fips'
columns: List[str] = [CITY_NAME_COLUMN, STATE_NAME_COLUMN, STATE_CODE_COLUMN, COUNTY_CODE_COLUMN]

# this dataset has some either old or invalid fips codes, so here we map the bad ones into the good ones
# why connecticut?? why!!! (copilot generated the values, so hopefully its correct :D)
INVALID_COUNTY_CODE_TO_CORRECT_COUNTY_CODE: Dict[str, str] = {
    "09110": "09011", # New London County, CT
    "09120": "09007", # Middlesex County, CT
    "09130": "09009", # New Haven County, CT
    "09140": "09001", # Fairfield County, CT
    "09160": "09005", # Litchfield County, CT
    "09170": "09003", # Hartford County, CT
    "09190": "09013", # Tolland County, CT
}

def createCity(city_name: str, state_name: str, state_code: str, county_code: str) -> City:
    if county_code in INVALID_COUNTY_CODE_TO_CORRECT_COUNTY_CODE:
        county_code = INVALID_COUNTY_CODE_TO_CORRECT_COUNTY_CODE[county_code]
    return City(city_name, state_name, state_code, county_code)


# some teams have no zip code, and the city is not in the city dataset, so we have to hardcode some of these :(
# copilot generated most of these because I was too lazy to look up the county codes myself, so hopefully they are correct
HARDCODED_CITIES: List[City] = [
    createCity("Walpole", "Massachusetts", "MA", "25021"),
    createCity("Medford", "Massachusetts", "MA", "25017"),
    createCity("Medford", "New Jersey", "NJ", "34005"),
    createCity("Woodbine", "Maryland", "MD", "24013"),
    createCity("Erie", "Michigan", "MI", "26059"),
    createCity("Sutton", "Massachusetts", "MA", "25027"),
    createCity("Wellesley Hills", "Massachusetts", "MA", "25021"),
    createCity("Devils Lake", "North Dakota", "ND", "38019"),
    createCity("Denville", "New Jersey", "NJ", "34027"),
    createCity("Lexington", "Massachusetts", "MA", "25017"),
    createCity("Scituate", "Massachusetts", "MA", "25023"),
    createCity("Dunbarton", "New Hampshire", "NH", "33013"),
    createCity("Palmer", "Massachusetts", "MA", "25013"),
    createCity("Toms River", "New Jersey", "NJ", "34029"),
    createCity("Saint Louis", "Missouri", "MO", "29510"),
    createCity("Bedford", "New Hampshire", "NH", "33011"),
    createCity("Ijamsville", "Maryland", "MD", "24031"),
    createCity("Fuquay Varina", "North Carolina", "NC", "37183"),
    createCity("Ozone Park", "New York", "NY", "36081"),
    createCity("Wayne", "New Jersey", "NJ", "34031"),
    createCity("Saint Johns", "Florida", "FL", "12109"),
    createCity("JACKSON JUNCTION", "Iowa", "IA", "19019"),
    createCity("Del Valle", "Texas", "TX", "48453"),
    createCity("Coeur D Alene", "Idaho", "ID", "16055"),
    createCity("Wilton", "Maine", "ME", "23017"),
    createCity("Kents Hill", "Maine", "ME", "23017"),
    createCity("Hanover", "Maryland", "MD", "24003"),
    createCity("Pleasant Valley", "Iowa", "IA", "19163"),
    createCity("Wynnewood", "Pennsylvania", "PA", "42045"),
    createCity("Stowe", "Vermont", "VT", "50015"),
    createCity("New Boston", "Michigan", "MI", "26163"),
    createCity("Coventry", "Rhode Island", "RI", "44003"),
    createCity("Arden", "North Carolina", "NC", "37121"),
    createCity("Rosemary Beach", "Florida", "FL", "12059"),
    createCity("West Newbury", "Massachusetts", "MA", "25009"),
    createCity("Kingwood", "Texas", "TX", "48201"),
    createCity("Clinton Township", "Michigan", "MI", "26099"),
    createCity("Bark River", "Michigan", "MI", "26041"),
    createCity("Covert", "Michigan", "MI", "26021"),
    createCity("Winston Salem", "North Carolina", "NC", "37169"),
    createCity("Montezuma", "New Mexico", "NM", "35045"),
    createCity("Christchurch", "Virginia", "VA", "51036"),
    createCity("Southampton", "New York", "NY", "36103"),
    createCity("Saint Augustine", "Florida", "FL", "12109"),
    createCity("Chesterfield", "Virginia", "VA", "51041"),
    createCity("Warwick", "New York", "NY", "36111"),
    createCity("Saint Petersburg", "Florida", "FL", "12103"),
    createCity("Redford", "Michigan", "MI", "26125"),
    createCity("Needham", "Massachusetts", "MA", "25021"),
    createCity("Kennebunk", "Maine", "ME", "23031"),
    createCity("Vestaburg", "Michigan", "MI", "26117"),
    createCity("Jerome", "Michigan", "MI", "26059"),
    createCity("Winnetka", "California", "CA", "06037"),
    createCity("Bridgewater", "Massachusetts", "MA", "25023"),
    createCity("Reading", "Massachusetts", "MA", "25017"),
    createCity("West Springfield", "Massachusetts", "MA", "25013"),
    createCity("Durham", "New Hampshire", "NH", "33017"),
    createCity("Salem", "New Hampshire", "NH", "33015"),
    createCity("Tabernacle", "New Jersey", "NJ", "34005"),
    createCity("Bensalem", "Pennsylvania", "PA", "42017"),
    createCity("Horsham", "Pennsylvania", "PA", "42091"),
    createCity("N. Charleston", "South Carolina", "SC", "45019"),
]

class CityDataset:
    def __init__(self, filepath):
        df = pd.read_csv(filepath, usecols=columns, dtype=str)
        self.__create_lookup_map(df)
        
    def __create_lookup_map(self, df: pd.DataFrame):
        # create a dict from ("city", "state_name") to City
        self.__lookup_map_state_name: Dict[Tuple[str, str], City] = {}
        # create a dict from ("city", "state_code") to City
        self.__lookup_map_state_code: Dict[Tuple[str, str], City] = {}
        
        for city in HARDCODED_CITIES:
            key = (city.get_city_name(), city.get_state_name())
            self.__lookup_map_state_name[key] = city
            key = (city.get_city_name(), city.get_state_code())
            self.__lookup_map_state_code[key] = city

        for _, row in df.iterrows():
            city_name: str = row[CITY_NAME_COLUMN]
            state_name: str = row[STATE_NAME_COLUMN]
            state_code: str = row[STATE_CODE_COLUMN]
            county_code: str = row[COUNTY_CODE_COLUMN]

            city = createCity(city_name, state_name, state_code, county_code)
            key: Tuple[str, str] = (city_name, state_name)
            self.__lookup_map_state_name[key] = city
            key: Tuple[str, str] = (city_name, state_code)
            self.__lookup_map_state_code[key] = city


    def get_city(self, city_name: str, state_name_or_code: str) -> Optional[City]:
        key = (city_name, state_name_or_code)
        if key in self.__lookup_map_state_name:
            return self.__lookup_map_state_name[key]
        if key in self.__lookup_map_state_code:
            return self.__lookup_map_state_code[key]
        return None
