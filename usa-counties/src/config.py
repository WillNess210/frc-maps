"""Config class for the project."""

from files import FilepathFactory


class Config:
    """Config class for the project."""

    def __init__(self, year: int):
        self.__year = year
        self.__filepaths = FilepathFactory(year)

    def get_filepaths(self):
        """Getter for the filepaths factory."""
        return self.__filepaths

    def get_year(self):
        """Getter for the year."""
        return self.__year


CONFIG = Config(2024)
