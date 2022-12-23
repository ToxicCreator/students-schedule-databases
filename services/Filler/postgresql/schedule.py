import os
import sys
from typing import List
from table import Table
from postgresql.psql_manager import PsqlManager
from utils import parse_data

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


class Schedule(Table):
    TABLE_NAME = 'schedule'

    def __init__(self, clear=False):
        self.psql = PsqlManager(
            os.getenv('POSTGRES_DBASE_IP'), os.getenv('POSTGRES_PORT_FIRST'),
            os.getenv('POSTGRES_DBASE_LOGIN'), os.getenv('POSTGRES_DBASE_PASSWORD')
        )
        if clear:
            self.clear()
        self.create_table()

    def create_table(self):
        query = f'''
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                id SERIAL PRIMARY KEY NOT NULL,
                date date NOT NULL,
                lesson_id int NOT NULL,
                group_id VARCHAR(10) NOT NULL
            );
        '''
        self.psql.execute_and_commit(query)
        self.__make_partition()

    def __make_partition(self):
        with open("postgresql/schedulePartitionCfg.txt") as file:
            self.psql.execute_and_commit(file.read())

    def insert(self, date, lesson_id, group_id):
        try:
            self.psql.insert(self.TABLE_NAME, {
                'date': date,
                'lesson_id': lesson_id,
                'group_id': group_id
            })
            return True
        except (Exception,):
            return False

    def read(self, schedule_id) -> List[tuple]:
        query = f'''
            SELECT * FROM {self.TABLE_NAME} 
            WHERE id = '{schedule_id}'
        '''
        self.psql.execute_and_commit(query)
        return self.psql.cursor.fetchall()

    def read_lessons_by_group(self, group_name):
        query = f'''
            SELECT lesson_id FROM {self.TABLE_NAME} 
            WHERE group_id = '{group_name}'
        '''
        self.psql.execute_and_commit(query)
        return self.psql.cursor.fetchall()

    def clear(self):
        self.psql.drop_table(self.TABLE_NAME)