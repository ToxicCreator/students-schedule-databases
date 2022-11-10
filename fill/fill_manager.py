import random
from faker import Faker

from mongo.institutes import Institutes
from postgresql.courses import Courses
from postgresql.groups import Groups
from postgresql.lessons import Lessons
from elastic.descriptions import Descriptions
from postgresql.groups_lessons import GroupsLessons
from redis_db.students import Students
from postgresql.visits import Visits

from utils import parse_data, check_chance, generate_group_name, get_lesson_date


TYPES = [
  'Лекция',
  'Практика',
  'Лабараторная'
]

def fill():
  Faker.seed(0)
  specialities_codes = __fill_institutes()

  courses_id = __fill_courses(specialities_codes, min_duration=10)
  groups_names = __fill_groups(specialities_codes)
  lessons_id = __fill_lessons(courses_id)
  groups_lessons = __fill_groups_lessons(groups_names, lessons_id)
  
  groups_students = __fill_students(groups_names, min=2, max=5)
  __fill_visits(groups_lessons, groups_students)


def __fill_institutes():
  institutes = Institutes(clear=True)
  institutes.fill()
  return institutes.get_specialities_codes()


def __fill_courses(specialities_codes, min_duration=2, max_duration=120) -> list:
  assert min_duration / 2 > 1
  assert max_duration >= min_duration and max_duration / 2 > 1
  courses_id = []
  courses = Courses(clear=True)
  data = parse_data('fill\courses.json')
  for i in range(len(specialities_codes)):
    code = specialities_codes[i]
    count = random.randint(1, len(data))
    cut_courses = random.choices(data, k=count)
    for course in cut_courses:
      duration = 2 * random.randint(min_duration / 2, max_duration / 2)
      courses_id.append(courses.insert(course['name'], code, duration))
  return courses_id


def __fill_groups(specialities_codes):
  groups_names = set()
  groups = Groups(clear=True)
  for i in range(len(specialities_codes)):
    code = specialities_codes[i]
    for group_number in range(1, random.randint(1, 4)):
      while True:
        group_name = generate_group_name(group_number)
        if group_name in groups_names:
          continue
        groups.insert(group_name, code)
        groups_names.add(group_name)
        break
  return list(groups_names)


def __fill_lessons(courses_id: list):
  lessons_id = []
  lessons = Lessons(clear=True)
  courses = Courses()
  descriptions = Descriptions(clear=True)
  for course_id in courses_id:
    duration = courses.get_duration(course_id)
    lesson_count = int(duration / 2)
    for lesson_number in range(1, lesson_count):
      type = random.choice(TYPES)
      lesson_date = get_lesson_date(lesson_number, lesson_count)
      lesson_id = lessons.insert(type, lesson_date, course_id)
      lessons_id.append(lesson_id)
      descriptions.insert(type, 'Описание', '', lesson_id)
  return lessons_id


def __fill_groups_lessons(groups_names, lessons_id):
  groups_lessons = GroupsLessons(clear=True)
  courses = Courses()
  lessons = Lessons()
  groups_lessons_map = {}
  for group_name in groups_names:
    groups_lessons_map[group_name] = []
    courses_id = courses.get_courses_by_group(group_name)
    lesson_course_id = lessons.read(lesson_id)[2]
    for lesson_id in lessons_id:
      if check_chance(70):
        groups_lessons.insert(group_name, lesson_id)
        groups_lessons_map[group_name].append(lesson_id)
  return groups_lessons_map


def __fill_students(groups_names, min=10, max=30):
  students = Students(clear=True)
  fake = Faker()
  groups_students = {}
  for group_name in groups_names:
    groups_students[group_name] = []
    count = random.randint(min, max)
    for i in range(count):
      student = students.insert(fake.name(), group_name)
      groups_students[group_name].append(student)
  return groups_students


def __fill_visits(groups_lessons, groups_students):
  visits = Visits(clear=True)
  for group_name in groups_lessons.keys():
    for lesson_id in groups_lessons[group_name]:
      for student_id in groups_students[group_name]:
        visited = check_chance(50)
        visits.insert(lesson_id, student_id, visited)
