# script which calls endpoint multiple times then dumps the data to a JSON file
import requests
import tbapy

BASE_URL = "https://api.frc-colors.com/v1/team"
MAX_FRC_COLORS_PAGE_SIZE = 100
YEAR = 2024

from dotenv import load_dotenv
import os


class Environment:
    def __init__(self):
        # Load the .env file
        load_dotenv()
        self.__TBA_KEY = os.getenv("TBA_KEY")

    def get_tba_key(self) -> str:
        if self.__TBA_KEY is None:
            raise ValueError("TBA_KEY is not defined in .env file")
        return self.__TBA_KEY


env = Environment()
TBA_KEY = env.get_tba_key()

tba = tbapy.TBA(TBA_KEY)
tba_teams = tba.teams(year=YEAR)
tba_team_keys = [tba_team.key[3:] for tba_team in tba_teams]
print("Example team: " + tba_team_keys[0])

tba_team_colors = {}

example = {
    "teams": {
        "254": {
            "teamNumber": 254,
            "colors": {
                "primaryHex": "#0070ff",
                "secondaryHex": "#232323",
                "verified": True,
            },
        },
        "581": {
            "teamNumber": 581,
            "colors": {
                "primaryHex": "#e86d38",
                "secondaryHex": "#7c7c7c",
                "verified": False,
            },
        },
        "1678": {"teamNumber": 1678, "colors": None},
    }
}

# step in batches of MAX_FRC_COLORS_PAGE_SIZE
for i in range(0, len(tba_team_keys), MAX_FRC_COLORS_PAGE_SIZE):
    tba_team_keys_batch = tba_team_keys[i : i + MAX_FRC_COLORS_PAGE_SIZE]
    full_url = BASE_URL + "?team=" + "&team=".join(tba_team_keys_batch)
    print("Fetching " + full_url)
    response = requests.get(full_url, timeout=5).json()  # Added timeout argument
    print("response: " + str(response))
    for team in response["teams"]:
        print("Parsing team " + team)
        team_obj = response["teams"][team]
        if "colors" in team_obj and team_obj["colors"] is not None:
            tba_team_colors[team] = team_obj["colors"]["primaryHex"]
        else:
            tba_team_colors[team] = None

# dump file
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
        with open(output_filepath, "w") as outfile:
            json.dump(data, outfile)
            print("Saved to " + output_filepath)


output_file_creator = OutputFileCreator()
output_file_creator.json_dump(tba_team_colors, "output/frc-colors.json")
