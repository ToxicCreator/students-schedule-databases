from neo4j_manager import Neo4jManager


class Graph():
  NODE_LABELS = {
    'course': 'course',
    'group': 'group',
    'student': 'student'
  }


  def __init__(self):
    self.client = Neo4jManager()
    self.client.clear_all()


  def fill(self):
    c1 = self.create_course_node('Технологии программирования')
    c2 = self.create_course_node('Физика')
    c3 = self.create_course_node('Курс по Web-программированию')

    group = self.create_group_node('БСБО-01-19', 4)

    s1 = self.create_student_node(11111, 'Болотов А.Ю.', 21)
    self.create_student_course_merge(s1, c1)
    self.create_student_course_merge(s1, c2)
    self.create_student_course_merge(s1, c3)
    self.create_student_group_merge(s1, group)
    s2 = self.create_student_node(22222, 'Трушин М.М.', 20)
    self.create_student_course_merge(s2, c1)
    self.create_student_course_merge(s2, c2)
    self.create_student_group_merge(s2, group)


  def create_course_node(self, name):
    label = self.NODE_LABELS['course']
    return self.client.create_node(label, {
      'name': name
    })


  def create_group_node(self, name, course):
    label = self.NODE_LABELS['group']
    return self.client.create_node(label, { 
      'name': name,
      'course': course
    })


  def create_student_node(self, id, name, age):
    label = self.NODE_LABELS['student']
    return self.client.create_node(label, { 
      'name': name,
      'id': id,
      'age': age
    })


  def create_student_course_merge(self, student, course):
    return self.client.create_merge(student, course, 'study')


  def create_student_group_merge(self, student, group):
    return self.client.create_merge(student, group, 'member')


  def print_all(self):
    records = self.client.read_all()
    for rec in records:
      rec = rec[0]
      print('\n\n\nid:', rec.id, '\t| labels:', list(rec.labels))
      print('--------------------------------------------')
      for key in rec.keys():
        print(f'{key}:', rec[key])
      print('____________________________________________')
