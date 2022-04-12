import sqlite3
from typing import Union
from src.base_connector import BaseConnector


class SqliteConnector(BaseConnector):

    def __init__(self, connection: str) -> None:
        super().__init__(connection=connection)
        self._con_str = connection
        self._db_connection = None
        self._cursor = None
    
    def __enter__(self):
        self._db_connection = sqlite3.connect(self._con_str)
        self._cursor = self._db_connection.cursor()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        try:
            self._db_connection.close()
        except Exception as e:
            print(f'Error on closing DB connection: {e}')
    
    def query(self, select: Union[list, dict], from_: str, where: dict):
        if isinstance(select, list):
            sel = ", ".join([name for name in select])
        elif isinstance(select, dict):
            sel = ", ".join(['{} as {}'.format(key, value) for key, value in select.items()])
        else:
            raise ValueError("'select' argument must be of type list or dict")
        
        if not isinstance(from_, str):
            from_ = str(from_)
        
        if not isinstance(where, dict):
            pass