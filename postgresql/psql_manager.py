import psycopg2

# docker run -d --name postgres-cnt -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgrespw postgres

class PsqlManager():
  def __new__(self):
    if not hasattr(self, 'instance'):
        self.instance = super(PsqlManager, self).__new__(self)
    return self.instance


  def __init__(self):
    self.connection = psycopg2.connect(
      database="postgres", 
      user="postgres", 
      password="postgrespw", 
      host="host.docker.internal", 
      port=49153
    )
    self.cursor = self.connection.cursor()


  def __del__(self):
    self.connection.close()


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
    query = f'SELECT * FROM {table_name}'
    query += self.__get_query_where_arguments(map_key_values)
    self.execute_and_commit(query)
    return self.cursor.fetchone()


  def __get_query_insert_arguments(self, map_key_values):
    query = f' ({", ".join(map_key_values.keys())})'
    for key in map_key_values:
      map_key_values[key] = str(map_key_values[key])
    values = map_key_values.values()
    query += f''' VALUES ('{"', '".join(values)}\')'''
    return query


  def __get_query_where_arguments(self, map_key_values):
    query = f' WHERE '
    arguments = []
    for key in map_key_values.keys():
      value = map_key_values[key]
      arguments.append(f"{key} = '{value}'")
    query += ' AND '.join(arguments)
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
    query = f'TRUNCATE {table_name};'
    self.execute_and_commit(query)


  def drop_table(self, table_name):
    query = f'DROP TABLE IF EXISTS {table_name} CASCADE;'
    self.execute_and_commit(query)
    print(f'Table "{table_name}" die.')