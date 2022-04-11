from abc import ABC, abstractmethod
from pandas import DataFrame


class BaseConnector(ABC):

    def __init__(self, connection: str) -> None:
        self._df = None
    
    @abstractmethod
    def __enter__(self):
        """ Enter context manager """
    
    @abstractmethod
    def __exit__(self):
        """ Safely exit context mananger """

    @property
    def data(self) -> DataFrame:
        return self._df