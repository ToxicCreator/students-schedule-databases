import os
import sys
from table import Table
from postgresql.psql_manager import PsqlManager
from utils import parse_data

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

class Groups(Table):
    TABLE_NAME = 'groups'

    def __init__(self, clear=False):
        settings = parse_data('settings.json')
        self.psql = PsqlManager(settings["host"], settings["postgresql"]["port"], 
                                settings["postgresql"]["login"], settings["postgresql"]["password"])
        self.graph = Graph()
        
        if clear:
            self.clear()
        self.create_table()

    def create_table(self) -> None:
        query = f'''
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                name VARCHAR(10) PRIMARY KEY NOT NULL,
                speciality_id VARCHAR(8) NOT NULL
            );
        '''
        self.psql.execute_and_commit(query)

    def insert(self, name, speciality_id):
        values = {
            'name': name,
            'speciality_id': speciality_id
        }
        self.psql.insert(self.TABLE_NAME, values)
        self.graph.create_group_node(name=name,
                                     spec_code=speciality_id)
        return name

    def read(self, name) -> tuple:
        query = f'''
            SELECT * FROM {self.TABLE_NAME} 
            WHERE name = {name}
        '''
        self.psql.execute_and_commit(query)
        return self.psql.cursor.fetchone()

    def read_by_speciality_id(self, spiciality_id):
        query = f'''
            SELECT name FROM {self.TABLE_NAME}
            WHERE speciality_id = '{spiciality_id}'
        '''
        self.psql.execute_and_commit(query)
        return self.psql.cursor.fetchall()

    def read_all_ids(self):
        query = f'''
            SELECT name FROM {self.TABLE_NAME};
        '''
        self.psql.execute_and_commit(query)
        return self.psql.cursor.fetchall()

    def clear(self) -> None:
        self.psql.drop_table(self.TABLE_NAME)

    def get_speciality(self, group_id) -> tuple:
        return self.read(group_id)[1]
