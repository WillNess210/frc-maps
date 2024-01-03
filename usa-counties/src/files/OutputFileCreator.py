import os
import json

class OutputFileCreator:
    def __init__(self):
        pass

    def __create_output_directory(self, output_filepath):
        output_directory = os.path.dirname(output_filepath)
        os.makedirs(output_directory, exist_ok=True)

    def json_dump(self, data, output_filepath):
        self.__create_output_directory(output_filepath)
        with open(output_filepath, 'w') as outfile:
            json.dump(data, outfile)
            print("Saved to " + output_filepath)