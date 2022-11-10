import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from table import Table
from postgresql.psql_manager import PsqlManager


class GroupsLessons(Table):
  TABLE_NAME = 'groups_lessons'

  def __init__(self, clear=False):
    self.psql = PsqlManager()
    if clear: self.clear()
    self.create_table()


  def create_table(self):
    query = f'''
      CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
        id SERIAL PRIMARY KEY NOT NULL,
        group_name VARCHAR(10) NOT NULL,
        lesson_id int NOT NULL
      );
    '''
    self.psql.execute_and_commit(query)


  def insert(self, group_name, lesson_id):
    try:
      self.psql.insert(self.TABLE_NAME, {
        'group_name': group_name,
        'lesson_id': lesson_id
      })
      return True
    except:
      return False


  def read(self, id):
    query = f'''
      SELECT * FROM {self.TABLE_NAME} 
      WHERE id = '{id}'
    '''
    self.psql.execute_and_commit(query)
    return self.psql.cursor.fetchall()


  def clear(self):
    self.psql.drop_table(self.TABLE_NAME)


  def get_lessons(self, group_name):
    query = f'''
      SELECT lesson_id FROM {self.TABLE_NAME} 
      WHERE group_name = '{group_name}'
    '''
    self.psql.execute_and_commit(query)
    return self.psql.cursor.fetchall()
