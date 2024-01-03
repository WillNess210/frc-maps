class County:
    def __init__(self, county):
        self.county = county

    def set_fill(self, r: int, g: int, b: int):
        self.county.attrib["fill"] = "rgb(" + str(r) + "," + str(g) + "," + str(b) + ")"

    def get_title(self):
        return self.county[0].text

    def set_title(self, title):
        self.county[0].text = title

    def add_hover_effect(self):
        # bold outline on hover
        # <path id="c06065" d="m176.23 369.3-1.7276 2.442-0.53843 0.933-0.49029 1.76-0.10519 0.747-0.54555 2.724-0.74881 2.603-2.3142 2.731-3.8154-0.763-2.4586-0.424-9.4813-1.858-11.557-2.418-4.0097-0.909-5.9227-1.285-4.081-0.892-7.5219-1.806 0.0891-0.387-2.0022-1.784-2.6993-0.619 0.13728-0.66 2.4586-2.401-0.9164-1.271-1.0679-0.401-0.55626-1.495-1.1963-2.718 0.62757-1.138 2.3534-2.034 2.66 0.603 0.72385 0.169 0.16046 0.385 2.4586 0.916 5.4805 1.22 2.4015 0.09 4.6693 0.82 13.532 2.86 9.4332 2 0.20239-1.0122 3.5434 0.69815 12.824 2.573" style="stroke:#000">
        #  <title>Riverside, CA</title>
        # </path>
        self.county.attrib["style"] = "stroke:#000"
        self.county.attrib["onmouseover"] = "this.style.strokeWidth='2';"
        self.county.attrib["onmouseout"] = "this.style.strokeWidth='1';"
        self.county.attrib["onclick"] = "alert(this.id);"