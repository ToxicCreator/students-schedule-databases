import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from table import Table
from postgresql.psql_manager import PsqlManager


class Courses(Table):
  TABLE_NAME = 'courses'

  def __init__(self, clear=False):
    self.psql = PsqlManager()
    if clear: self.clear()
    self.create_table()


  def create_table(self):
    query = f'''
      CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
        id SERIAL PRIMARY KEY NOT NULL,
        name VARCHAR(120) NOT NULL,
        sp_code VARCHAR(8) NOT NULL,
        duration int NOT NULL
      );
    '''
    self.psql.execute_and_commit(query)


  def insert(self, name, sp_code, duration):
    values = {
      'name': name,
      'sp_code': sp_code,
      'duration': duration
    }
    return self.psql.insert(self.TABLE_NAME, values)[0]


  # def get_id(self, name, specialitiesCode, duration):
  #   query = f'''
  #     SELECT id FROM {self.TABLE_NAME} 
  #     WHERE name = {name}
  #     AND specialitiesCode = {specialitiesCode}
  #     AND duration = {duration}
  #   '''
  #   self.psql.execute_and_commit(query)
  #   return self.psql.cursor.fetchall()


  def read(self, id):
    query = f'''
      SELECT * FROM {self.TABLE_NAME} 
      WHERE id = {id}
    '''
    self.psql.execute_and_commit(query)
    return self.psql.cursor.fetchall()


  def clear(self):
    self.psql.clear_table(self.TABLE_NAME)


  def get_duration(self, id):
    return self.read(id)[0][3]


  def get_courses_by_group(self, group_name):
    query = f'''
      SELECT {self.TABLE_NAME}.id FROM {self.TABLE_NAME} 
      JOIN groups 
        ON {self.TABLE_NAME}.sp_code = groups.code 
      WHERE groups.name = '{group_name}';
    '''
    self.psql.execute_and_commit(query)
    return self.psql.cursor.fetchall()

