from json import load
from datetime import date
from random import randint, choices


def parse_data(file_path):
<<<<<<< Updated upstream
    with open(file_path, encoding='utf-8') as file:
=======
    with open(file_path, encoding = 'utf-8') as file:
>>>>>>> Stashed changes
        return load(file)


def check_chance(chance) -> bool:
<<<<<<< Updated upstream
    if chance < 1: chance * 100
=======
    if chance < 1:
        chance * 100
>>>>>>> Stashed changes
    return randint(0, 100) <= chance


def generate_group_name(number) -> str:
    letter = ['А', 'Б', 'В', 'Г', 'Д']
<<<<<<< Updated upstream
    name = choices(letter, k=4)
=======
    name = choices(letter, k = 4)
>>>>>>> Stashed changes
    name += f'-{number}'
    return ''.join(name)


<<<<<<< Updated upstream
def get_lesson_date(lesson_number, lesson_count, year=2022):
    day = randint(1, 28)
    month = lesson_number // (lesson_count / 12)
    if month == 0: month = 1
    return date(year, int(month), day)
=======
def get_lesson_date(lesson_number, lesson_count, year = 2022):
    day = randint(1, 28)
    month = lesson_number // (lesson_count / 12)
    if month == 0:
        month = 1
    return date(year, int(month), day)
>>>>>>> Stashed changes
