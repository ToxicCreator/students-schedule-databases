import random
from faker import Faker
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from neo4j_db.graph import Graph
from mongo.institutes import Institutes
from postgresql.courses import Courses
from postgresql.groups import Groups
from postgresql.lessons import Lessons
from elastic.descriptions import Descriptions
from postgresql.groups_lessons import GroupsLessons
from redis_db.students import Students
from postgresql.visits import Visits
from names import get_first_name, get_last_name
from utils import parse_data, check_chance, generate_group_name, get_lesson_date

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

TYPES = [
  'Лекция',
  'Практика',
  'Лабараторная'
]

def fill():
    Faker.seed(0)
    # graph = Graph()
    # graph.clear()
    # specialities_codes = __fill_institutes()
    # courses_id = __fill_courses(specialities_codes, min_duration=2, max_duration=4)
    # groups_names = __fill_groups(specialities_codes)
    # __fill_lessons(courses_id)
    __fill_students(groups_names=group_names, min=10, max=20)
    # __fill_visits(groups_names)


def __fill_institutes():
    institutes = Institutes(clear=True)
    institutes.fill()
    return institutes.get_specialities_codes()


def __fill_courses(specialities_codes, min_duration=2, max_duration=120) -> list:
    assert min_duration / 2 >= 1
    assert max_duration >= min_duration and max_duration / 2 > 1
    courses_id = []
    courses = Courses(clear=True)
    data = parse_data('fill/courses.json')
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
    lessons = Lessons(clear=True)
    descriptions = Descriptions(clear=True)
    groups_lessons = GroupsLessons(clear=True)
    courses = Courses()
    for course_id in courses_id:
        duration = courses.get_duration(course_id)
        lesson_count = int(duration / 2)
        groups = courses.get_groups(course_id)
        for group in groups:
            for lesson_number in range(1, lesson_count + 1):
                type = random.choice(TYPES)
                lesson_date = get_lesson_date(lesson_number, lesson_count)
                lesson_id = lessons.insert(type, lesson_date, course_id)
            descriptions.insert(type, 'Описание', '', lesson_id)
            groups_lessons.insert(group[0], lesson_id)


def __fill_students(groups_names, min = 10, max = 30):
    settings = parse_data('../settings.py')
    students = Students(settings["host"], settings["redis"]["port"], clear=True)
    fake = Faker()
    groups_students = {}
    for group_name in groups_names:
        groups_students[group_name] = []
        count = random.randint(min, max)
        for i in range(count):
            student = students.insert(name=get_first_name(), surname=get_last_name(), group_name=group_name)
            groups_students[group_name].append(student)
    return groups_students


def __fill_visits(groups_names):
    visits = Visits(clear=True)
    students = Students()
    groups_lessons = GroupsLessons()
    for group_name in groups_names:
        for lesson in groups_lessons.get_lessons(group_name):
            for student_id in students.get_by_group(group_name):
                visited = check_chance(50)
                visits.insert(lesson[0], student_id, visited)
