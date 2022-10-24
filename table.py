from abc import ABC, abstractmethod


class Table(ABC):
  @property
  def TABLE_NAME(self):
    pass

  @abstractmethod
  def insert(self, *args):
    NotImplemented
  
  @abstractmethod
  def update(self, search, new_value):
    NotImplemented

  @abstractmethod
  def read(self, search):
    NotImplemented

  @abstractmethod
  def fill(self, count):
    NotImplemented

  @abstractmethod
  def print(self, searchID):
    NotImplemented

  @abstractmethod
  def print_all(self):
    NotImplemented

  @abstractmethod
  def clear(self):
    NotImplemented