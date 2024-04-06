"""A module to generate filepaths for the project."""

import os

PROJECT_ROOT_DIRECTORY_NAME = "usa-counties"


class MapAndTableOutputFilepaths:
    """A class to store the output filepaths for a map and table."""

    def __init__(self, output_prefix: str):
        self.__generate_map_output(output_prefix)
        self.__generate_table_output(output_prefix)

    def __generate_map_output(self, output_prefix: str):
        self.__map_output = os.path.join(output_prefix, "output.svg")

    def __generate_table_output(self, output_prefix: str):
        self.__table_output = os.path.join(output_prefix, "output.md")

    def get_map_output(self) -> str:
        """Get the output filepath for the map"""
        return self.__map_output

    def get_table_output(self) -> str:
        """Get the output filepath for the table"""
        return self.__table_output


class FilepathFactory:
    """A class to generate filepaths for the project."""

    def __init__(self, year: int):
        self.year = str(year)
        self.prefix = self.__get_path_to_usa_counties_root()

    def __get_path_to_usa_counties_root(self) -> str:
        # get the current working directory, up to `usa-counties/src`
        # ex: "/home/user/usa-counties/src/a/" => "/home/user/usa-counties/src"
        current_directory = os.getcwd()
        index = current_directory.find(PROJECT_ROOT_DIRECTORY_NAME)
        if index == -1:
            raise Exception("Could not find the project root directory")
        return current_directory[: index + len(PROJECT_ROOT_DIRECTORY_NAME)]

    def __get_path_to(self, *args) -> str:
        return os.path.join(self.prefix, *args)

    def get_county_location_dataset_filepath(self) -> str:
        """Get the path to the county location dataset file"""
        return self.__get_path_to("assets", "counties_loc.csv")

    def get_usa_counties_svg_filepath(self) -> str:
        """Get the path to the USA counties SVG file"""
        return self.__get_path_to("assets", "usa_counties.svg")

    def get_us_cities_filepath(self) -> str:
        """Get the path to the US cities file"""
        return self.__get_path_to("assets", "uscities.csv")

    def get_zipcodes_filepath(self) -> str:
        """Get the path to the ZIP codes file"""
        return self.__get_path_to("assets", "ZIP-COUNTY-FIPS_2017-06.csv")

    def get_team_key_to_frc_color_filepath(self) -> str:
        """Get the path to the FRC colors output file"""
        return self.__get_path_to(
            "src", "output", "frc-colors", self.year, "frc-colors.json"
        )

    def get_team_key_to_county_codes_filepath(self) -> str:
        """Get the path to the team key to county codes file"""
        return self.__get_path_to(
            "src",
            "output",
            "team_locations",
            self.year,
            "team_key_to_county_codes.json",
        )

    def get_team_list_filepath(self) -> str:
        """Get the path to the team list file"""
        return self.__get_path_to(
            "src", "output", "team_list", self.year, "team_keys.json"
        )

    def get_team_density_output_filepaths(self) -> MapAndTableOutputFilepaths:
        """Get the output filepaths for the team density map and table"""
        return MapAndTableOutputFilepaths(
            self.__get_path_to("src", "output", "team_density_map", self.year)
        )

    def get_event_key_to_county_codes_filepath(self) -> str:
        """Get the path to the event key to county codes file"""
        return self.__get_path_to(
            "src",
            "output",
            "event_locations",
            self.year,
            "event_key_to_county_codes.json",
        )

    def get_event_density_output_filepaths(self) -> MapAndTableOutputFilepaths:
        """Get the output filepaths for the event density map and table"""
        return MapAndTableOutputFilepaths(
            self.__get_path_to("src", "output", "event_density_map", self.year)
        )

    def get_starting_ownership_filepath(self) -> str:
        """Get the path to the starting ownership file"""
        return self.__get_path_to(
            "src", "output", "starting_ownership", self.year, "starting_ownership.json"
        )

    def get_ownership_map_output_filepaths(self) -> MapAndTableOutputFilepaths:
        """Get the output filepaths for the ownership map and table"""
        return MapAndTableOutputFilepaths(
            self.__get_path_to("src", "output", "ownership_map", self.year)
        )

    def get_precomputed_county_distance_filepath(self) -> str:
        """Get the path to the precomputed county distance file"""
        return self.__get_path_to(
            "src",
            "output",
            "precomputed-county-distance",
            "precomputed-county-distance.json",
        )
