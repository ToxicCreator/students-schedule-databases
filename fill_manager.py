import random
from faker import Faker
from datetime import date

from mongo.institutes import Institutes
from postgresql.groups import Groups
from postgresql.visits import Visits
from redis_db.students import Students
from postgresql.lessons import Lessons
from elastic.descriptions import Descriptions
from postgresql.groups_lessons import GroupsLessons

from utils import check_chance, generate_group_name


TYPES = [
  'Лекция',
  'Практика',
  'Лабараторная'
]

def fill():
  Faker.seed(0)
  specialities_codes, courses_id = __fill_institutes()
  
  groups_names = __fill_groups(specialities_codes)
  lessons_id = __fill_lessons(courses_id, max=10)
  groups_lessons = __fill_groups_lessons(groups_names, lessons_id)
  
  groups_students = __fill_students(groups_names)
  __fill_visits(groups_lessons, groups_students)


def __fill_institutes():
  institutes = Institutes()
  institutes.fill()
  return (
    institutes.get_specialities_codes(), 
    institutes.get_courses_id()
  )


def __fill_groups(specialities_codes):
  groups_names = []
  groups = Groups()
  for i in range(len(specialities_codes)):
    for group_number in range(1, random.randint(1, 4)):
      code = specialities_codes[i]
      is_inserted = False
      group_name = None
      while not is_inserted:
        group_name = generate_group_name(group_number)
        is_inserted = groups.insert(group_name, code)
      groups_names.append(group_name)
  return groups_names


def __fill_lessons(courses_id, min=1, max=1):
  lessons_id = []
  lessons = Lessons()
  # descriptions = Descriptions()
  for course_id in courses_id:
    for lesson_number in range(min, random.randint(min, max)):
      type = random.choice(TYPES)
      day = random.randint(1, 28)
      lesson_date = date(2022, lesson_number, day)
      lessons.insert(type, lesson_date, course_id)
      lesson = lessons.read(type, lesson_date, course_id)
      lesson_id = lesson[0][0]
      lessons_id.append(lesson_id)
      # descriptions.insert()
  return lessons_id


def __fill_groups_lessons(groups_names, lessons_id):
  groups_lessons = GroupsLessons()
  groups_lessons_map = {}
  for group_name in groups_names:
    groups_lessons_map[group_name] = []
    for lesson_id in lessons_id:
      if check_chance(70):
        groups_lessons.insert(group_name, lesson_id)
        groups_lessons_map[group_name].append(lesson_id)
  return groups_lessons_map


def __fill_students(groups_names):
  students = Students()
  fake = Faker()
  groups_students = {}
  for group_name in groups_names:
    groups_students[group_name] = []
    count = random.randint(10, 30)
    for i in range(count):
      student = students.insert(fake.name(), group_name)
      groups_students[group_name].append(student)
  return groups_students


def __fill_visits(groups_lessons, groups_students):
  visits = Visits()
  for group_name in groups_lessons.keys():
    for lesson_id in groups_lessons[group_name]:
      for student_id in groups_students[group_name]:
        visited = check_chance(50)
        visits.insert(lesson_id, student_id, visited)
