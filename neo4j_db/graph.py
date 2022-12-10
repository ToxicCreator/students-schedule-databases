import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from neo4j_db.neo4j_manager import Neo4jManager
from utils import parse_data




class Graph:
    def __init__(self):
        settings = parse_data('settings.json')
        self.client = Neo4jManager(settings["host"], settings["neo4j"]["port"],
                                   settings["neo4j"]["login"], settings["neo4j"]["password"])

    def create_institute_node(self, name):
        return self.client.create_node('institute', {
            'name': name
        })

    def create_department_node(self, name):
        return self.client.create_node('department',
                                       {'Name': name})

    def create_speciality_node(self, name, code, department_name):
        query = f'''
            MATCH (d:department {{Name: '{department_name}'}})
            CREATE (s:speciality)-[:belongs_to]->(d)
            SET s = $params
            RETURN s;
        '''
        return self.client.execute(query, {
            'Name': name,
            'Code': code
        }).single()

    def create_course_node(self, name, department_name):
        query = f'''
            MATCH (d:department {{Name: '{department_name}'}})
            CREATE (c:course)-[:is_taught_by]->(d)
            SET c = $params
            RETURN c;
        '''
        return self.client.execute(query, {
            'Name': name
        }).single()

    def create_group_node(self, name, spec_code):
        query = f'''
                   MATCH (s:speciality {{Code: '{spec_code}'}})
                   CREATE (g:group)-[:member_of]->(s)
                   SET g = $params;
               '''
        return self.client.execute(query, {
            'Name': name
        }).single()

    def create_student_node(self, recordbook, group_name):
        query = f'''
            MATCH (g:group {{Name: '{group_name}'}})
            CREATE (st:student)-[:member]->(g)
            SET st = $params;
        '''
        return self.client.execute(query, {
            'RecordBook': recordbook
        }).single()

    def create_visit_node(self, lesson_id, student_id, visited):
        rel = 'unvisited'
        if visited:
            rel = 'visited'
        query = f'''
            MATCH (l:lesson {{id: {lesson_id}}}) WITH l
            MATCH (s:student {{id: '{student_id}'}})
            CREATE (s)-[r:{rel}]->(l)
            RETURN l, s, r;
        '''
        return self.client.execute(query).single()

    def create_student_course_tie(self, group_name, course_names):
        query = f'''
            MATCH (g:group {{Name: '{group_name}'}})<-[:member]-(st:student) WITH st
            MATCH (c:course) WHERE c.Name IN {course_names} 
            CREATE (st)-[:studying]->(c)'''
        self.client.execute(query, {}).single()

    def create_lesson_node(self, lesson_id, course_name):
        query = f'''
           MATCH (c:course {{Name: '{course_name}'}})
           CREATE (l:lesson)-[:part_of]->(c)
           SET l = $params
           RETURN l;
        '''
        return self.client.execute(query, {
            'Id': lesson_id
        }).single()


    def clear(self):
        self.client.clear_all()
