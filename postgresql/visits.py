import os
import sys
from postgresql.psql_manager import PsqlManager
from table import Table
from neo4j_db.graph import Graph

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


class Visits(Table):
    TABLE_NAME = 'visits'

    def __init__(self, clear = False):
        self.psql = PsqlManager()
        self.graph = Graph()
        if clear:
            self.clear()
        self.create_table()

    def create_table(self):
        query = f'''
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                lesson INT NULL,
                student VARCHAR(9) NOT NULL,
                visited BOOLEAN DEFAULT false
            );
        '''
        self.psql.execute_and_commit(query)

    def insert(self, lesson_id, student_id, visited = False):
        map_key_values = {
            'lesson': lesson_id,
            'student': student_id,
            'visited': visited
        }
        self.psql.insert(self.TABLE_NAME, map_key_values)
        self.graph.create_visit_node(lesson_id, student_id, visited)

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
