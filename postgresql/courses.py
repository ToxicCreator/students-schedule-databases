import os
import sys

from typing import List

from table import Table
from postgresql.psql_manager import PsqlManager
from neo4j_db.graph import Graph

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


class Courses(Table):
    TABLE_NAME = 'courses'

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
                name VARCHAR(120) NOT NULL,
                duration int NOT NULL
            );
        '''
        self.psql.execute_and_commit(query)

    def insert(self, name, duration):
        values = {
            'name': name,
            'duration': duration
        }
        course_id = self.psql.insert(self.TABLE_NAME, values)[0]
        self.graph.create_course_node(course_id, values)
        return course_id

    # def get_id(self, name, specialitiesCode, duration):
    #   query = f'''
    #     SELECT id FROM {self.TABLE_NAME}
    #     WHERE name = {name}
    #     AND specialitiesCode = {specialitiesCode}
    #     AND duration = {duration}
    #   '''
    #   self.psql.execute_and_commit(query)
    #   return self.psql.cursor.fetchall()

    def read(self, course_id) -> List[tuple]:
        query = f'''
        SELECT * FROM {self.TABLE_NAME} 
        WHERE id = {course_id}
        '''
        self.psql.execute_and_commit(query)
        return self.psql.cursor.fetchall()

    def clear(self) -> None:
        self.psql.drop_table(self.TABLE_NAME)

    def get_duration(self, course_id) -> List[tuple]:
        return self.read(course_id)[0][3]

    def get_courses_by_group(self, group_name) -> List[tuple]:
        query = f'''
            SELECT {self.TABLE_NAME}.id FROM {self.TABLE_NAME} 
            JOIN groups 
                ON {self.TABLE_NAME}.sp_code = groups.code 
            WHERE groups.name = '{group_name}';
        '''
        self.psql.execute_and_commit(query)
        return self.psql.cursor.fetchall()

    def get_groups(self, course_id) -> List[tuple]:
        query = f'''
            SELECT groups.name as group 
            FROM courses 
                JOIN groups ON courses.sp_code = groups.code
            WHERE courses.id = {course_id}
            GROUP BY groups.name;
        '''
        self.psql.execute_and_commit(query)
        return self.psql.cursor.fetchall()
