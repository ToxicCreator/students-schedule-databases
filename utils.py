from json import load
from datetime import date
from random import randint, choices, choice

def parse_data(file_path):
    with open(file_path, encoding = 'utf-8') as file:
        return load(file)


def check_chance(chance) -> bool:
    if chance < 1:
        chance * 100
    return randint(0, 100) <= chance


def generate_group_name() -> str:
    letters = "БСБОКМПФРСГУДИЭХТВ"

    groupCode = ''.join(choice(letters) for i in range(4))
    groupCode += "-0"
    groupCode += str(randint(1, 9))
    groupCode += "-"
    groupCode += str(randint(18, 22))
    return groupCode


def get_lesson_date(
        lesson_number, 
        lessons_count,
        months_count, 
        first_year
    ):
    assert lesson_number <= lessons_count
    assert 1990 <= first_year <= 2022
    assert 1 <= months_count <= 45
    day = randint(1, 28)
    month_number = lesson_number // (lessons_count / (months_count - 1)) + 9
    year = int(month_number // 13) + first_year
    month = month_number % 12
    if month == 0:
        month = 12
    return date(year, int(month), day)


def get_foreign_courses(own_department_id, department_courses):
    foreign_courses = []

    for department_id in department_courses:
        if department_id != own_department_id:
            foreign_courses.extend(department_courses[department_id])

    return foreign_courses
