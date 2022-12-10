from abc import ABC, abstractmethod


class Table(ABC):
    @property
    def TABLE_NAME(self):
        pass

    @abstractmethod
    def insert(self, *args):
        NotImplemented

    @abstractmethod
    def read(self, *args):
        NotImplemented

    @abstractmethod
    def clear(self):
        NotImplemented
