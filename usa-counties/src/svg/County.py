class County:
    def __init__(self, county):
        self.__county = county
        self.__name = self.get_title()
        self.__fips = county.attrib["id"][1:]

    def set_fill(self, r: int, g: int, b: int):
        self.__county.attrib["fill"] = (
            "rgb(" + str(r) + "," + str(g) + "," + str(b) + ")"
        )

    def set_fill_color(self, color: str):
        self.__county.attrib["fill"] = color

    def get_title(self):
        return self.__county[0].text

    def get_name(self):
        return self.__name

    def get_fips(self):
        return self.__fips

    def set_title(self, title):
        self.__county[0].text = title
