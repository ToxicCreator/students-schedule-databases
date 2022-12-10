import os
import sys
from postgresql.psql_manager import PsqlManager
from table import Table
from utils import parse_data

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


class Visits(Table):
    TABLE_NAME = 'visits'

    def __init__(self, clear=False):
        self.psql = PsqlManager(os.getenv('POSTGRES_DBASE_IP'), os.getenv('POSTGRES_PORT_FIRST'),
                                os.getenv('POSTGRES_DBASE_LOGIN'), os.getenv('POSTGRES_DBASE_PASSWORD'))
        if clear:
            self.clear()
        self.create_table()

    def create_table(self):
        query = f'''
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                id serial PRIMARY KEY NOT NULL,
                shedule_id int NOT NULL,
                student_id VARCHAR(7) NOT NULL,
                date date NOT NULL,
                visited boolean NOT NULL
            );
        '''
        self.psql.execute_and_commit(query)
        self.__make_partition()

    def __make_partition(self):
        with open("postgresql/visitsPartitionCfg.txt") as file:
            self.psql.execute_and_commit(file.read())

    def insert(self, shedule_id, student_id, date, visited = False):
        map_key_values = {
            'shedule_id' : shedule_id,
            'student_id' : student_id,
            'date' : date,
            'visited': visited
        }
        self.psql.insert(self.TABLE_NAME, map_key_values)

    def read(self, studentID, lessonID):
        query = f'''
            SELECT * FROM {self.TABLE_NAME} 
            WHERE student = {studentID} 
            AND lesson = {lessonID}
        '''
        self.psql.execute_and_commit(query)
        return self.psql.cursor.fetchall()

    def clear(self):
        self.psql.drop_table(self.TABLE_NAME)
