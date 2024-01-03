from dotenv import load_dotenv
import os

class Environment:
    def __init__(self):
        # Load the .env file
        load_dotenv()
        self.__TBA_KEY = os.getenv('TBA_KEY')

    def get_tba_key(self) -> str:
        if self.__TBA_KEY is None:
            raise ValueError('TBA_KEY is not defined in .env file')
        return self.__TBA_KEY
