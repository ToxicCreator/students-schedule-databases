from psql_manager import PsqlManager
from table import Table
from datetime import date
from faker import Faker
import random


week_count = 53

class Lessons(Table):
  TABLE_NAME = 'lessons'
  TYPES = {
    'practica': 'Практика',
    'lecture': 'Лекция',
    'labaratory': 'Лабараторная'
  }
  NAMES = [
    'Математический анализ',
    'Физика',
    'История',
    'Технологии программирования',
    'Линейная алгебра'
  ]

  def __init__(self):
    self.psql = PsqlManager()
    if not self.psql.check_table_exist(self.TABLE_NAME):
      self.create_table()
    self.create_partition()


  def __del__(self):
    self.clear()


  def get_types(self):
    return self.TYPES


  def create_table(self):
    query = f'''
      CREATE TABLE {self.TABLE_NAME} (
        id SERIAL PRIMARY KEY NOT NULL,
        type VARCHAR(40) NOT NULL,
        date TIMESTAMP NOT NULL,
        name VARCHAR(70) NOT NULL
      );
    '''
    self.psql.execute_and_commit(query)


  def create_partition(self):
    for week_number in range (1, week_count):
      part_name = f'{self.TABLE_NAME}{week_number}'
      if self.psql.check_table_exist(part_name):
        continue
      print(f'Create partition "{part_name}"')
      query = f'''
        CREATE TABLE {part_name} (
          CHECK ( date_part('week', date) = {week_number})
        ) INHERITS ({self.TABLE_NAME})
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
          date_part('week', NEW.date)::integer
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

  def insert(self, type, date, name):
    self.psql.insert(self.TABLE_NAME, {
      'type': type,
      'date': date,
      'name': name
    })


  def read_by_id(self, id):
    query = f'''
      SELECT * FROM {self.TABLE_NAME} 
      WHERE id = {id}
    '''
    self.psql.execute_and_commit(query)
    return self.psql.cursor.fetchall()


  def read(self, search):
    query = f'''
      SELECT * FROM {self.TABLE_NAME} 
      WHERE type = '{search['type']}' 
        AND date = '{search['date']}' 
        AND name = '{search['name']}'
    '''
    self.psql.execute_and_commit(query)
    return self.psql.cursor.fetchall()


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
        date = '{date}'
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


  def fill(self, count):
    Faker.seed(0)
    fake = Faker()
    for _ in range(count):
      random_type_key = random.choice(list(self.TYPES.keys()))
      random_type = self.TYPES[random_type_key]
      
      random_date = fake.date_between(
        date(2022, 1, 1), 
        date(2022, 12, 31)
      )

      random_name = random.choice(self.NAMES)
      
      self.insert(random_type, random_date, random_name)


  def clear(self):
    for week_number in range (1, week_count):
      self.psql.clear_table(f'{self.TABLE_NAME}{week_number}')
    self.psql.clear_table(self.TABLE_NAME)


  def print(self, id):
    rows = self.read_by_id(id)
    print('---------------------------')
    for row in rows:
      print('type =', row[1])
      print('date =', row[2])
      print('name =', row[3])
      print('---------------------------')


  def print_all(self):
    rows = self.psql.select_all(self.TABLE_NAME)
    print('Table:', self.TABLE_NAME)
    print('---------------------------')
    for row in rows:
      print('type =', row[1])
      print('date =', row[2])
      print('name =', row[3])
      print('---------------------------')
