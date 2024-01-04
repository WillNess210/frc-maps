import pandas as pd
from .City import City
from typing import Dict, Tuple, List, Optional

# only keeping a subset of the columns to save memory
CITY_NAME_COLUMN = 'city'
STATE_NAME_COLUMN = 'state_name'
COUNTY_CODE_COLUMN = 'county_fips'
columns: List[str] = [CITY_NAME_COLUMN, STATE_NAME_COLUMN, COUNTY_CODE_COLUMN]

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

def createCity(city_name: str, state_name: str, county_code: str) -> City:
    if county_code in INVALID_COUNTY_CODE_TO_CORRECT_COUNTY_CODE:
        county_code = INVALID_COUNTY_CODE_TO_CORRECT_COUNTY_CODE[county_code]
    return City(city_name, state_name, county_code)


# some teams have no zip code, and the city is not in the city dataset, so we have to hardcode some of these :(
# copilot generated most of these because I was too lazy to look up the county codes myself, so hopefully they are correct
HARDCODED_CITIES: List[City] = [
    # city, state, county code
    createCity("Walpole", "Massachusetts", "25021"),
    createCity("Medford", "Massachusetts", "25017"),
    createCity("Medford", "New Jersey", "34005"),
    createCity("Woodbine", "Maryland", "24013"),
    createCity("Erie", "Michigan", "26059"),
    createCity("Sutton", "Massachusetts", "25027"),
    createCity("Wellesley Hills", "Massachusetts", "25021"),
    createCity("Devils Lake", "North Dakota", "38019"),
    createCity("Denville", "New Jersey", "34027"),
    createCity("Lexington", "Massachusetts", "25017"),
    createCity("Scituate", "Massachusetts", "25023"),
    createCity("Dunbarton", "New Hampshire", "33013"),
    createCity("Palmer", "Massachusetts", "25013"),
    createCity("Toms River", "New Jersey", "34029"),
    createCity("Saint Louis", "Missouri", "29510"),
    createCity("Bedford", "New Hampshire", "33011"),
    createCity("Ijamsville", "Maryland", "24031"),
    createCity("Fuquay Varina", "North Carolina", "37183"),
    createCity("Ozone Park", "New York", "36081"),
    createCity("Wayne", "New Jersey", "34031"),
    createCity("Saint Johns", "Florida", "12109"),
    createCity("JACKSON JUNCTION", "Iowa", "19019"),
    createCity("Del Valle", "Texas", "48453"),
    createCity("Coeur D Alene", "Idaho", "16055"),
    createCity("Wilton", "Maine", "23017"),
    createCity("Kents Hill", "Maine", "23017"),
    createCity("Hanover", "Maryland", "24003"),
    createCity("Pleasant Valley", "Iowa", "19163"),
    createCity("Wynnewood", "Pennsylvania", "42045"),
    createCity("Stowe", "Vermont", "50015"),
    createCity("New Boston", "Michigan", "26163"),
    createCity("Coventry", "Rhode Island", "44003"),
    createCity("Arden", "North Carolina", "37121"),
    createCity("Rosemary Beach", "Florida", "12059"),
    createCity("West Newbury", "Massachusetts", "25009"),
    createCity("Kingwood", "Texas", "48201"),
    createCity("Clinton Township", "Michigan", "26099"),
    createCity("Bark River", "Michigan", "26041"),
    createCity("Covert", "Michigan", "26021"),
    createCity("Winston Salem", "North Carolina", "37169"),
    createCity("Montezuma", "New Mexico", "35045"),
    createCity("Christchurch", "Virginia", "51036"),
    createCity("Southampton", "New York", "36103"),
    createCity("Saint Augustine", "Florida", "12109"),
    createCity("Chesterfield", "Virginia", "51041"),
    createCity("Warwick", "New York", "36111"),
    createCity("Saint Petersburg", "Florida", "12103"),
    createCity("Redford", "Michigan", "26125"),
    createCity("Needham", "Massachusetts", "25021"),
    createCity("Kennebunk", "Maine", "23031"),
    createCity("Vestaburg", "Michigan", "26117"),
    createCity("Jerome", "Michigan", "26059"),
    createCity("Winnetka", "California", "06037")
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
            city = createCity(city_name, state_name, county_code)
            self.__lookup_map[key] = city

    def get_city(self, city_name: str, state_name: str) -> Optional[City]:
        key = (city_name, state_name)
        if key in self.__lookup_map:
            return self.__lookup_map[key]
        return None
