import sqlite3
from typing import Union
from pandas import DataFrame
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
    
    def run_query(self, select: Union[list, dict], from_: str, where: dict):
        if isinstance(select, list):
            sel_stm = ", ".join([name for name in select])
        elif isinstance(select, dict):
            sel_stm = ", ".join(['{col} as {alias}'.format(col=key, alias=value) for key, value in select.items()])
        else:
            raise TypeError("'select' argument must be of type list or dict")
        
        if not isinstance(from_, str):
            from_ = str(from_)
        

        query_stm = f"SELECT {sel_stm} FROM {from_} WHERE {where}"
        self._cursor.execute(query_stm)
        result = self._cursor.fetchall()
        self._cursor.close()
        self._df = DataFrame(columns=[select], data=result)
        print(self._df)

