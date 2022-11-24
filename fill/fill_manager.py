import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import random
#from faker import Faker
# from neo4j_db.graph import Graph
from mongo.institutes import Institutes
from postgresql.shedule import Shedule
from postgresql.groups import Groups
from postgresql.lessons import Lessons
# from elastic.descriptions import Descriptions
from redis_db.students import Students
from postgresql.visits import Visits

from utils import parse_data, check_chance, generate_group_name, get_lesson_date

TYPES = [
    'Лекция',
    'Практика',
]

def fill():
    #Faker.seed(0)
    # graph = Graph()
    # graph.clear()

    institutes = __fill_institutes()

    groups = __fill_groups(institutes.get_specialities_codes())
    lessons = __fill_lessons(institutes.get_courses_ids())
    shedule =  __fill_shedule(institutes, lessons, groups)
    # __fill_visits(groups_names)


def __fill_institutes():
    institutes = Institutes(clear = True)
    institutes.fill('fill/mongoInit.json')
    return institutes

def __fill_groups(specialities_codes):
    groups = Groups(clear = True)

    for id in specialities_codes:
        for groups_count in range(random.randint(2, 5)):
            groups.insert(generate_group_name(), id)
    return groups
    
def __fill_lessons(courses_id: list):
    lessons = Lessons(clear = True)

    for id in courses_id:
        for lection_num in range(1, 9):
            lessons.insert(TYPES[0], id)
        for practic_num in range(1, 17):
            lessons.insert(TYPES[1], id)
    
    return lessons


def __fill_shedule(institutes, lessons, groups):
    deps_courses = institutes.get_departments_courses()
    deps_specialities = institutes.get_departments_cpecialities()

# def __fill_students(groups_names, min = 10, max = 30):
#     settings = parse_data('settings.py')
#     students = Students(settings["host"], settings["redis"]["port"], clear = True)
#     fake = Faker()
#     groups_students = {}
#     for group_name in groups_names:
#         groups_students[group_name] = []
#         count = random.randint(min, max)
#         for i in range(count):
#             student = students.insert(fake.name(), group_name)
#             groups_students[group_name].append(student)
#     return groups_students


# def __fill_visits(groups_names):
#     visits = Visits(clear = True)
#     students = Students()
#     groups_lessons = GroupsLessons()
#     for group_name in groups_names:
#         for lesson in groups_lessons.get_lessons(group_name):
#             for student_id in students.get_by_group(group_name):
#                 visited = check_chance(50)
#                 visits.insert(lesson[0], student_id, visited)
