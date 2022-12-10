import os
import sys
from postgresql.psql_manager import PsqlManager
from table import Table
from neo4j_db.graph import Graph
from utils import parse_data


currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


class Students(Table):
    TABLE_NAME = 'students'

    def __init__(self, clear = False):
        self.psql = PsqlManager(os.getenv('POSTGRES_DBASE_IP'), os.getenv('POSTGRES_PORT_FIRST'),
                                os.getenv('POSTGRES_DBASE_LOGIN'), os.getenv('POSTGRES_DBASE_PASSWORD'))
        if clear:
            self.clear()
        self.create_table()

    def create_table(self):
        query = f'''
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                id VARCHAR(7) PRIMARY KEY NOT NULL,
                group_id VARCHAR(10) NOT NULL,
                name VARCHAR(30) NOT NULL,
                surname VARCHAR(30) NOT NULL
            );
        '''
        self.psql.execute_and_commit(query)

    def read(self, student_id):
        query = f'''
            SELECT * FROM {self.TABLE_NAME} 
            WHERE id = '{student_id}'
        '''
        self.psql.execute_and_commit(query)
        return self.psql.cursor.fetchall()


    def insert(self, student_id, group_id, name, surname):
        map_key_values = {
            'id' : student_id,
            'group_id' : group_id,
            'name' : name,
            'surname': surname
        }
        self.psql.insert(self.TABLE_NAME, map_key_values)

    def clear(self):
        self.psql.drop_table(self.TABLE_NAME)
