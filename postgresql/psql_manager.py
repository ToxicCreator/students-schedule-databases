import psycopg2


class PsqlManager():
  def __new__(self):
    if not hasattr(self, 'instance'):
      self.instance = super(PsqlManager, self).__new__(self)
    return self.instance


  def __init__(self, settings=None):
    self.connection = psycopg2.connect(
      database="postgres", 
      user="postgres", 
      password="postgrespw", 
      host="host.docker.internal", 
      port="5050"
    )
    print("PostgreSQL connected successfully.")
    self.cursor = self.connection.cursor()


  def execute_and_commit(self, query):
    self.cursor.execute(query)
    self.connection.commit()


  def check_table_exist(self, table_name):
    query = f'''
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_name = '{table_name}' 
      AND table_schema 
      NOT IN ('information_schema','pg_catalog');
    '''
    self.execute_and_commit(query)
    return not (self.cursor.rowcount == 0)


  def insert(self, table_name, map_key_values):
    query = f'INSERT INTO {table_name}'
    query += self.__get_query_insert_arguments(map_key_values)
    self.execute_and_commit(query)


  def __get_query_insert_arguments(self, map_key_values):
    query = f' ({", ".join(map_key_values.keys())})'
    for key in map_key_values:
      map_key_values[key] = str(map_key_values[key])
    values = map_key_values.values()
    query += f''' VALUES ('{"', '".join(values)}\')'''
    return query


  def select_all(self, table_name):
    query = f'''
      SELECT * FROM {table_name}
    '''
    self.execute_and_commit(query)
    return self.cursor.fetchall() 


  def clear_table(self, table_name):
    if not self.check_table_exist(table_name):
      return
    query = f'''
      TRUNCATE {table_name};
    '''
    self.execute_and_commit(query)
    print(f'Table "{table_name}" clear.')


  def drop_table(self, table_name):
    query = f'''
      DROP TABLE IF EXISTS {table_name};
    '''
    self.execute_and_commit(query)
    print(f'Table "{table_name}" die.')