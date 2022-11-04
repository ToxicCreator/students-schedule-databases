from datetime import date
from neo4j_db.graph import Graph
from mongo.groups import Groups
from postgresql.visits import Visits
from postgresql.lessons import Lessons
from redis_db.students import Students
from elastic.descriptions import Descriptions


def mongo():
  print('\n--== MongoDB ==--')
  groups = Groups()

  print('\nCreate & read all:')
  groups.fill(3)
  groups.read_all()

  print('\nRead one:')
  groups.read({'name': 'БСБО-02-19'})

  print('\nUpdate one:')
  filter = {'name': 'БСБО-02-19'}
  new_value = { '$set': { 'course': 5 } }
  groups.update(filter, new_value)
  groups.read({'name': 'БСБО-02-19'})

  print('\nDelete all groups')
  groups.clear()
  groups.read_all()


def redis():
  print('\n--== Redis ==--')
  students = Students()

  print('\nCreate & read all:')
  students.fill(5)
  students.print_all()
  
  print('\nRead one:')
  shifr = list(students.get_shifrs())[0]
  students.print(shifr)

  print('\nUpdate one:')
  new_value = students.read(shifr)
  new_value['FIO'] = 'Студент'
  students.update(shifr, new_value)
  students.print(shifr)
  
  print('\nDelete all students')
  students.clear()
  students.print_all()


def postgres():
  print('\n--== PostgreSQL ==--')
  visits = Visits()
  lessons = Lessons()

  print('\nCreate & read all:')
  visits.fill(5)
  visits.print_all()
  
  print('\nCreate and read one:')
  visits.insert('12345', '1')
  visits.print('12345', '1')

  print('\nCreate & read all:')
  lessons.fill(5)
  lessons.print_all()

  print('\nCreate & Update one:')
  type = lessons.get_types()['lecture']
  new_date = date.today()
  name = 'Философия'
  lessons.insert(type, new_date, name)
  id = lessons.read({
    'type': type,
    'lesson_date': new_date,
    'name': name
  })[0][0]
  lessons.update(id, name='Физика')
  lessons.print(id)


def elastic():
  print('\n--== ElasticSearch ==--')
  desc = Descriptions()

  print('\nCreate & read all:')
  desc.fill()
  desc.print_all()

  print('\nRead:')
  desc.print({
    "Name": "Математический анализ",
    "Type": "Лекция"
  })

  print('\nUpdate value:')
  desc.update({
    "Name": "Математический анализ",
    "Type": "Лекция"
  }, {
    "Name": "Матанализ"
  })
  desc.print_all()

  print('\nDelete:')
  desc.delete({
    "Name": "Технологии программирования"
  })
  desc.print_all()


def neo4j():
  graph = Graph()
  graph.fill()
  graph.print_all()


def main():
  # mongo()
  # redis()
  postgres()
  # elastic()
  # neo4j()


if __name__ == "__main__":
  main()