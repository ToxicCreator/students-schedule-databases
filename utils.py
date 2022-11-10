from json import load
from datetime import date
from random import randint, choices


def parse_data(file_path):
  with open(file_path, encoding='utf-8') as file:
    return load(file)


def check_chance(chance) -> bool:
  if chance < 1: chance * 100
  return randint(0, 100) <= chance


def generate_group_name(number) -> str:
  letter = ['А', 'Б', 'В', 'Г', 'Д']
  name = choices(letter, k=4)
  name += f'-{number}'
  return ''.join(name)


def get_lesson_date(lesson_number, lesson_count, year=2022):
  day = randint(1, 28)
  month = lesson_number // (lesson_count / 12)
  if month == 0: month = 1
  return date(year, int(month), day)