from random import randint, choices

def check_chance(chance) -> bool:
  if chance < 1: chance * 100
  return randint(0, 100) <= chance


def generate_group_name(number) -> str:
  letter = ['А', 'Б', 'В', 'Г', 'Д']
  name = choices(letter, k=4)
  name += f'-{number}'
  return ''.join(name)