import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import random
from neo4j_db.graph import Graph
from mongo.institutes import Institutes
from postgresql.schedule import Schedule
from postgresql.groups import Groups
from postgresql.lessons import Lessons
from elastic.descriptions import Descriptions
from postgresql.visits import Visits
import redis_db.students
import postgresql.students
from names import get_first_name, get_last_name
from utils import parse_data, check_chance, generate_group_name, get_lesson_date, get_foreign_courses

TYPES = [
  'Лекция',
  'Практика'
]

def fill():
    institutes = __fill_institutes()
    print('institutes ready')
    groups = __fill_groups(institutes.get_specialities_codes())
    print('groups ready')
    lessons = __fill_lessons(institutes.get_courses_ids(), institutes)
    print('lessons ready')
    schedule, groups_schedule = __fill_schedule(institutes, lessons, groups)
    print('schedule ready')
    groups_students = __fill_students(groups.read_all_ids(), schedule, lessons, institutes)
    print('students ready')
    __fill_visits(groups_schedule, groups_students)
    print('visits ready')
    return True


def __fill_institutes():
    institutes = Institutes(clear=True)
    institutes.parse_institutes(path='fill/mongoInit.json')
    institutes.fill()
    institutes.make_neo4j_shortcuts()
    return institutes

def __fill_groups(specialities_codes):
    groups = Groups(clear=True)
    for id in specialities_codes:
        for groups_count in range(2, 5):
            group_name = generate_group_name()
            groups.insert(group_name, id)
    return groups
    
def __fill_lessons(courses_id: list, institutes):
    courses_names = institutes.get_course_names_by_ids(courses_id)
    lessons = Lessons(clear=True)
    descriptions = Descriptions()
    for i in range(len(courses_id)):
        for lection_num in range(6, 12):
            lessons.insert(TYPES[0], courses_id[i], courses_names[i], descriptions.insert())
        for practic_num in range(8, 16):
            lessons.insert(TYPES[1], courses_id[i], courses_names[i], descriptions.insert())
    return lessons

def __fill_schedule(institutes, lessons, groups):
    schedule = Schedule(clear=True)

    deps_courses = institutes.get_departments_courses()
    deps_specialities = institutes.get_departments_specialities()

    groups_schedule = {}

    current_schedule_id = 1

    for department in deps_specialities:
        specialities = deps_specialities[department]
        own_courses = deps_courses[department]
        foreign_courses = get_foreign_courses(department, deps_courses)

        for speciality_id in specialities:
            current_groups = groups.read_by_speciality_id(speciality_id)
            current_foreign_courses = random.choices(foreign_courses, k=8)
            own_lessons = lessons.read_by_course_ids(own_courses)
            foreign_lessons = lessons.read_by_course_ids(current_foreign_courses)

            for group in current_groups:
                group_id = group[0]
                first_year = random.choice([2017, 2018, 2019, 2020])
                groups_schedule[group_id] = []

                for i in range(len(own_lessons)):
                    lesson_id = own_lessons[i][0]
                    date = get_lesson_date(
                        lesson_number=i,
                        lessons_count=len(own_lessons),
                        months_count=45,
                        first_year=first_year
                    )
                    groups_schedule[group_id].append([current_schedule_id, date])
                    schedule.insert(date, lesson_id, group_id)
                    current_schedule_id += 1

                for i in range(len(foreign_lessons)):
                    lesson_id = foreign_lessons[i][0]
                    date = get_lesson_date(
                        lesson_number=i,
                        lessons_count=len(foreign_lessons),
                        months_count=45,
                        first_year=first_year
                    )
                    groups_schedule[group_id].append([current_schedule_id, date])
                    schedule.insert(date, lesson_id, group_id)
                    current_schedule_id += 1

    return schedule, groups_schedule


def __fill_students(groups, schedule, lessons, institutes, min=15, max=30):
    graph = Graph()
    redis_students = redis_db.students.Students(
        host=str(os.getenv('REDIS_DBASE_IP')),
        port=os.getenv('REDIS_DBASE_PORT'), 
        clear=True
    )
    postgres_students = postgresql.students.Students(clear=True)
    groups_students = {}
    for group in groups:
        group_name = group[0]
        groups_students[group_name] = []
        for i in range(random.randint(min, max)):
            name = get_first_name()
            surname = get_last_name()
            student = redis_students.insert(name=name, surname=surname, group_name=group_name)
            groups_students[group_name].append(student)
            postgres_students.insert(student, group_name, name, surname)
            
        lesson_ids = [lesson[0] for lesson in schedule.read_lessons_by_group(group_name)]
        courses = [course[0] for course in lessons.read_by_lesson_ids(lesson_ids)]
        course_names = institutes.get_course_names_by_ids(courses)
        graph.create_student_course_tie(group_name=group_name, course_names=course_names)
        
    return groups_students


def __fill_visits(groups_schedule, groups_students):
    visits = Visits(clear=True)
    schedule = Schedule()
    graph = Graph()
    i = 0
    for group in groups_schedule:
        for schedule_id_date in groups_schedule[group]:
            for student in groups_students[group]:
                schedule_id = schedule_id_date[0]
                lesson_id = schedule.read(schedule_id)[0][2]
                visit_id = visits.insert(schedule_id, student, schedule_id_date[1], check_chance(90))
                graph.create_visit_node(visit_id, lesson_id)


if __name__ == "__main__":
    fill()
