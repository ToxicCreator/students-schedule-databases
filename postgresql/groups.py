import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from table import Table
from postgresql.psql_manager import PsqlManager


class Groups(Table):
  TABLE_NAME = 'groups'

  def __init__(self, clear=False):
    self.psql = PsqlManager()
    if clear: self.clear()
    self.create_table()


  def create_table(self):
    query = f'''
      CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
        name VARCHAR(10) PRIMARY KEY NOT NULL,
        code VARCHAR(8) NOT NULL
      );
    '''
    self.psql.execute_and_commit(query)


  def insert(self, name, code):
    values = {
      'name': name,
      'code': code
    }
    if self.psql.insert(self.TABLE_NAME, values):
      return name
    return False


  def read(self, name):
    query = f'''
      SELECT * FROM {self.TABLE_NAME} 
      WHERE name = {name}
    '''
    self.psql.execute_and_commit(query)
    return self.psql.cursor.fetchone()


  def clear(self):
    self.psql.clear_table(self.TABLE_NAME)


  def get_speciality(self, id):
    return self.read(id)[1]
