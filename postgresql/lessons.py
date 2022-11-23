import os
import sys
import random
from postgresql.psql_manager import PsqlManager
from table import Table
from neo4j_db.graph import Graph

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


TYPES = [
    'Лекция',
    'Практика',
    'Лабораторная'
]

class Lessons(Table):
    TABLE_NAME = 'lessons'

    def __init__(self, clear = False):
        self.psql = PsqlManager()
        self.graph = Graph()
        if clear:
            self.clear()
        self.create_table()

    def create_table(self) -> None:
        query = f'''
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                id SERIAL PRIMARY KEY NOT NULL,
                type VARCHAR(40) NOT NULL,
                description_id SMALLINT NOT NULL,
                course_id SMALLINT NOT NULL
            );
        '''
        self.psql.execute_and_commit(query)

    def insert(self, description_id, course_id):
        lesson_type = random.choice(TYPES)
        values = {
            'type': lesson_type,
            'description_id': description_id,
            'course_id': course_id
        }
        lesson_id = self.psql.insert(self.TABLE_NAME, values)[0]
        self.graph.create_lesson_node(lesson_id, course_id, values)
        return lesson_id

    def read(self, lesson_id) -> tuple:
        query = f'''
            SELECT * FROM {self.TABLE_NAME} 
            WHERE id = {lesson_id}
        '''
        self.psql.execute_and_commit(query)
        return self.psql.cursor.fetchone()

    def clear(self) -> None:
        self.psql.drop_table(self.TABLE_NAME)

    def get_course(self, course_id) -> tuple:
        return self.read(course_id)[3]
