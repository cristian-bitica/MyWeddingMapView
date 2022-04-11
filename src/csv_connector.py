
from src.base_connector import BaseConnector
import pandas as pd


class CsvConnector(BaseConnector):

    def __init__(self, connection: str) -> None:
        super().__init__(connection=connection)

        self.__conn_str = connection
    
    def __enter__(self):
        self._df = pd.read_csv(self.__conn_str)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        return exc_traceback
    