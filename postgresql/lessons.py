import os
import sys
from postgresql.psql_manager import PsqlManager
from table import Table
from neo4j_db.graph import Graph
from utils import parse_data

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

week_count = 53

class Lessons(Table):
    TABLE_NAME = 'lessons'

    def __init__(self, clear=False):
        settings = parse_data('settings.json')
        self.psql = PsqlManager(settings["host"], settings["postgresql"]["port"], 
                                settings["postgresql"]["login"], settings["postgresql"]["password"])
        self.graph = Graph()
        if clear:
            self.clear()
        self.create_table()

    def create_table(self) -> None:
        query = '''
            DROP TYPE IF EXISTS lessType;
            CREATE TYPE lessType AS ENUM ('Практика', 'Лекция');
        '''

        self.psql.execute_and_commit(query)

        query = f'''
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                id SERIAL PRIMARY KEY NOT NULL,
                type lessType NOT NULL,
                course_id SMALLINT NOT NULL,
                description_id VARCHAR(50) NOT NULL
            );
        '''
        self.psql.execute_and_commit(query)

    def insert(self, lesson_type, course_id, course_name, description_id):
        values = {
            'type': lesson_type,
            'course_id': course_id,
            'description_id': description_id
        }
        lesson_id = self.psql.insert(self.TABLE_NAME, values)[0]
        self.graph.create_lesson_node(lesson_id, course_name)
        return lesson_id

    def read(self, lesson_id) -> tuple:
        query = f'''
            SELECT * FROM {self.TABLE_NAME} 
            WHERE id = {lesson_id}
        '''
        self.psql.execute_and_commit(query)
        return self.psql.cursor.fetchone()
    

    def read_by_course_ids(self, course_ids):
        query = f'''
            SELECT id FROM {self.TABLE_NAME} 
            WHERE course_id = {' OR course_id = '.join([str(course) for course in course_ids])} 
            GROUP BY course_id, id
        '''
        self.psql.execute_and_commit(query)
        return self.psql.cursor.fetchall()
        
    def read_by_lesson_ids(self, lesson_ids):
        query = f'''
                   SELECT DISTINCT course_id FROM {self.TABLE_NAME} 
                   WHERE id = {' OR id = '.join([str(lesson) for lesson in lesson_ids])} 
               '''
        self.psql.execute_and_commit(query)
        return self.psql.cursor.fetchall()

    def update(self, lesson_id, name=False, lesson_type = False, course_id = False) -> None:
        if lesson_type:
            self.update_type(lesson_id, lesson_type)
        if course_id:
            self.update_course_id(lesson_id, lesson_type)

    def update_type(self, lesson_id, lesson_type) -> None:
        query = f'''
            UPDATE {self.TABLE_NAME} set
                type = '{lesson_type}'
            WHERE id = {lesson_id}
        '''
        self.psql.execute_and_commit(query)

    def update_course_id(self, lesson_id, course_id) -> None:
        query = f'''
            UPDATE {self.TABLE_NAME} set
                course_id = {course_id}
            WHERE id = {lesson_id}
        '''
        self.psql.execute_and_commit(query)

    def clear(self) -> None:
        self.psql.drop_table(self.TABLE_NAME)

    def get_course(self, course_id) -> tuple:
        return self.read(course_id)[3]
