import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import json
import random
import pprint
from table import Table
from mongo.mongo_manager import MongoManager


database_name = 'prac_3'
collection_name = 'institutes'

class Institutes():
  def __init__(self):
    self.mongo = MongoManager(database_name)
    self.mongo.remove_collection(collection_name)
    self.collection = self.mongo.collection(collection_name)


  def fill(self):
    institutes = self.__parse_data('mongo\institutes.json')
    if isinstance(institutes, list):
      self.collection.insert_many(institutes)
    else:
      self.collection.insert_one(institutes)
    
    courses = self.__parse_data('mongo\courses.json')
    cut = random.randint(1, len(courses))
    self.collection.update_many(
      {},
      [{ '$set': { 'departments.specialities.courses': courses[:cut] } }]
    )


  def __parse_data(self, file_path):
    with open(file_path, encoding='utf-8') as file:
      return json.load(file)


  def get_specialities_codes(self):
    codes = []
    institutes = self.collection.find({}, {
      'departments.specialities': 1
    })
    for institute in institutes:
      for department in institute['departments']:
        for speciality in department['specialities']:
          codes.append(speciality['code'])
    return codes


  def get_courses_id(self):
    courses_id = []
    institutes = self.collection.find({}, {
      'departments.specialities.courses': 1
    })
    for institute in institutes:
      for department in institute['departments']:
        for speciality in department['specialities']:
          for course in speciality['courses']:
            courses_id.append(course['_id'])
    return courses_id


  def read_all(self):
    for group in self.collection.find({}, {'_id': 0}):
      pprint.pprint(group)


  def read(self, filter):
    group = self.collection.find_one(filter, {'_id': 0})
    pprint.pprint(group)


  def clear(self):
    self.collection.delete_many({})


  def update(self, filter, new_value):
    self.collection.update_one(filter, new_value)

