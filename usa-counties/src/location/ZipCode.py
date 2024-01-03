class ZipCode:
    def __init__(self, zipcode: str, county_code: str):
        self.__zipcode = zipcode
        self.__county_code = county_code

    def get_zipcode(self) -> str:
        return self.__zipcode
    
    def get_county_code(self) -> str:
        return self.__county_code