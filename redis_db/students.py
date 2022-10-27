import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from table import Table
import random
import redis


class Students(Table):
  def __init__(self):
    self.redis_db = redis.Redis(
      host='localhost', 
      port=6379, 
      db=0, 
      charset='UTF-8',
      decode_responses=True
    )
    self.shifrs = set()


  def get_shifrs(self):
    return self.shifrs


  def fill(self, count):
    for i in range(1, count+1):
      key = self.__get_shifr()
      self.insert(key, f'Студент №{i}', f'21.10.200{i}')


  def print_all(self):
    keys = self.redis_db.keys('*')
    for key in keys:
      self.print(key)


  def print(self, key):
    student = self.read(key)
    print(key, student)


  def read(self, key):
    return self.redis_db.hgetall(key)


  def insert(self, key, fio, birthdate):
    self.redis_db.hset(key, 'FIO', fio)
    self.redis_db.hset(key, 'Birthdate', birthdate)


  def update(self, key, new_value):
    self.redis_db.hmset(key, new_value)


  def clear(self):
    keys = self.redis_db.keys('*')
    for key in keys:
      self.redis_db.delete(key)


  def __get_shifr(self):
    shifr = [random.choice('АБВГ') for _ in range(3)]
    shifr.append('-')
    shifr += [random.choice('0123456789') for _ in range(5)]
    shifr = ''.join(shifr)
    if shifr in self.shifrs:
      return self.__get_shifr()
    self.shifrs.add(shifr)
    return shifr
