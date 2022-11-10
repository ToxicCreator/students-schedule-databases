import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import random
from faker import Faker
from datetime import date
from postgresql.psql_manager import PsqlManager
from table import Table


week_count = 53

class Lessons(Table):
  TABLE_NAME = 'lessons'

  def __init__(self, clear=False):
    self.psql = PsqlManager()
    if clear: self.clear()
    self.create_table()
    self.create_partition()


  def create_table(self):
    query = f'''
      CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
        id SERIAL PRIMARY KEY NOT NULL,
        type VARCHAR(40) NOT NULL,
        lesson_date TIMESTAMP NOT NULL,
        courseID SMALLINT NOT NULL
      );
    '''
    self.psql.execute_and_commit(query)


  def create_partition(self):
    for week_number in range (1, week_count):
      part_name = f'{self.TABLE_NAME}{week_number}'
      if week_number == 43:
        print()
      if self.psql.check_table_exist(part_name):
        continue
      query = f'''
        CREATE TABLE IF NOT EXISTS {part_name} (
          CHECK (date_part('week', lesson_date) = {week_number})
        ) INHERITS ({self.TABLE_NAME});
      '''
      self.psql.execute_and_commit(query)
    self.create_partition_trigger()

  def create_partition_trigger(self):
    trigger_name = 'insertPartition'
    trigger = f'''
      CREATE OR REPLACE FUNCTION {trigger_name}()
        RETURNS TRIGGER AS
      $$
      DECLARE
        partition_name TEXT;
      BEGIN
        partition_name := format(
          '{self.TABLE_NAME}%s', 
          date_part('week', NEW.lesson_date)::integer
        );
        execute 'INSERT INTO ' || partition_name || ' VALUES (($1).*)' USING NEW;
        RETURN null;
      END;
      $$
      LANGUAGE 'plpgsql';
    '''
    self.psql.execute_and_commit(trigger)
    query = f'''
      CREATE OR REPLACE TRIGGER partitionInsert 
      BEFORE INSERT ON {self.TABLE_NAME} 
      FOR EACH ROW EXECUTE PROCEDURE {trigger_name}();
    '''
    self.psql.execute_and_commit(query)


  def insert(self, type, lesson_date, courseID):
    return self.psql.insert(self.TABLE_NAME, {
      'type': type,
      'lesson_date': lesson_date,
      'courseID': courseID
    })[0]


  def read(self, id):
    query = f'''
      SELECT * FROM {self.TABLE_NAME} 
      WHERE id = {id}
    '''
    self.psql.execute_and_commit(query)
    return self.psql.cursor.fetchone()


  def update(self, id, type=False, date=False, name=False):
    if type: self.update_type(id, type)
    if date: self.update_date(id, date)
    if name: self.update_name(id, name)


  def update_type(self, id, type):
    query = f'''
      UPDATE {self.TABLE_NAME} set
        type = '{type}'
      WHERE id = {id}
    '''
    self.psql.execute_and_commit(query)


  def update_date(self, id, date):
    query = f'''
      UPDATE {self.TABLE_NAME} set
        lesson_date = '{date}'
      WHERE id = {id}
    '''
    self.psql.execute_and_commit(query)


  def update_name(self, id, name):
    query = f'''
      UPDATE {self.TABLE_NAME} set
        name = '{name}'
      WHERE id = {id}
    '''
    self.psql.execute_and_commit(query)


  def clear(self):
    self.psql.drop_table(self.TABLE_NAME)


  def get_course(self, id):
    return self.read(id)[3]