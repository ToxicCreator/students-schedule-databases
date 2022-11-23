import os
import sys
from postgresql.psql_manager import PsqlManager
from table import Table
from neo4j_db.graph import Graph

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

week_count = 53


class Lessons(Table):
    TABLE_NAME = 'lessons'

    def __init__(self, clear = False):
        self.psql = PsqlManager()
        self.graph = Graph()
        if clear:
            self.clear()
        self.create_table()
        self.create_partition()

    def create_table(self) -> None:
        query = f'''
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                id SERIAL PRIMARY KEY NOT NULL,
                type VARCHAR(40) NOT NULL,
                lesson_date TIMESTAMP NOT NULL,
                course_id SMALLINT NOT NULL
            );
        '''
        self.psql.execute_and_commit(query)

    def create_partition(self) -> None:
        for week_number in range(1, week_count):
            part_name = f'{self.TABLE_NAME}{week_number}'
            if week_number == 43:
                print()
            if self.psql.check_table_exist(part_name):
                continue
            query = f'''
                CREATE TABLE IF NOT EXISTS {part_name} (
                    CHECK (date_part('week', lesson_date) = {week_number})
                ) INHERITS ({self.TABLE_NAME});
            '''
            self.psql.execute_and_commit(query)
        self.create_partition_trigger()

    def create_partition_trigger(self) -> None:
        trigger_name = 'insertPartition'
        trigger = f'''
            CREATE OR REPLACE FUNCTION {trigger_name}()
                RETURNS TRIGGER AS
            $$
            DECLARE
                partition_name TEXT;
            BEGIN
                partition_name := format(
                    '{self.TABLE_NAME}%s', 
                    date_part('week', NEW.lesson_date)::integer
                );
                execute 'INSERT INTO ' || partition_name || ' VALUES (($1).*)' USING NEW;
                RETURN null;
            END;
            $$
            LANGUAGE 'plpgsql';
        '''
        self.psql.execute_and_commit(trigger)
        query = f'''
            CREATE OR REPLACE TRIGGER partitionInsert 
            BEFORE INSERT ON {self.TABLE_NAME} 
            FOR EACH ROW EXECUTE PROCEDURE {trigger_name}();
        '''
        self.psql.execute_and_commit(query)

    def insert(self, lesson_type, lesson_date, course_id):
        values = {
            'type': lesson_type,
            'lesson_date': lesson_date,
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

    def update(self, lesson_id, lesson_type = False, date = False, name = False) -> None:
        if lesson_type:
            self.update_type(lesson_id, lesson_type)
        if date:
            self.update_date(lesson_id, date)
        if name:
            self.update_name(lesson_id, name)

    def update_type(self, lesson_id, lesson_type) -> None:
        query = f'''
            UPDATE {self.TABLE_NAME} set
                type = '{lesson_type}'
            WHERE id = {lesson_id}
        '''
        self.psql.execute_and_commit(query)

    def update_date(self, lesson_id, date) -> None:
        query = f'''
            UPDATE {self.TABLE_NAME} set
                lesson_date = '{date}'
            WHERE id = {lesson_id}
        '''
        self.psql.execute_and_commit(query)

    def update_name(self, lesson_id, name) -> None:
        query = f'''
            UPDATE {self.TABLE_NAME} set
                name = '{name}'
            WHERE id = {lesson_id}
        '''
        self.psql.execute_and_commit(query)

    def clear(self) -> None:
        self.psql.drop_table(self.TABLE_NAME)

    def get_course(self, course_id) -> tuple:
        return self.read(course_id)[3]
