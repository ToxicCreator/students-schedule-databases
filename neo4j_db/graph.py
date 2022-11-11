import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from neo4j_db.neo4j_manager import Neo4jManager


class Graph():
  def __init__(self):
    self.client = Neo4jManager()


  def create_institute_node(self, name):
    return self.client.create_node('institute', {
      'name': name
    })


  def create_department_node(self, name, institute_name):
    query = f'''
      MATCH (i:institute {{name: '{institute_name}'}})
      CREATE (d:department)-[:in]->(i)
      SET d = $params
      RETURN d;
    '''
    return self.client.execute(query, {
      'name': name
    }).single()


  def create_speciality_node(self, code, name, department_name):
    query = f'''
      MATCH (d:department {{name: '{department_name}'}})
      CREATE (s:speciality)-[:in]->(d)
      SET s = $params
      RETURN s;
    '''
    return self.client.execute(query, {
      'code': code,
      'name': name
    }).single()


  def create_course_node(self, id, values):
    values['id'] = id
    query = f'''
      MATCH (s:speciality {{code: '{}'}})
      CREATE (c:course)-[:in]->(s)
      SET c = $params
      RETURN c;
    '''
    return self.client.execute(query, values).single()


  def create_lesson_node(self, id, course_id, values):
    query = f'''
      MATCH (c:course {{id: {course_id}}})
      CREATE (l:lesson)-[:in]->(c)
      SET l = $params;
    '''
    values['id'] = id
    return self.client.execute(query, values).single()


  def create_group_node(self, name, code):
    return self.client.create_node('group', { 
      'name': name,
      'code': code
    })


  def create_student_node(self, id, name, group_name):
    query = f'''
      MATCH (g:group {{name: '{group_name}'}})
      CREATE (s:student)-[:member]->(g)
      SET s = $params;
    '''
    return self.client.execute(query, { 
      'id': id,
      'name': name,
      'group_name': group_name
    }).single()


  def create_visit_node(self, lesson_id, student_id, visited):
    rel = 'unvisited'
    if visited: rel = 'visited'
    query = f'''
      MATCH (l:lesson {{id: {lesson_id}}}) WITH l
      MATCH (s:student {{id: '{student_id}'}})
      CREATE (s)-[r:{rel}]->(l)
      RETURN l, s, r;
    '''
    return self.client.execute(query).single()


  def clear(self):
    self.client.clear_all()
