class County:
    def __init__(self, county):
        self.county = county

    def set_fill(self, r: int, g: int, b: int):
        self.county.attrib["fill"] = "rgb(" + str(r) + "," + str(g) + "," + str(b) + ")"

    def set_title(self, title):
        self.county[0].text = title
