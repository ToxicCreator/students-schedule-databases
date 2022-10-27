import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import pprint
from table import Table
from mongo.mongo_manager import MongoManager


collection_name = 'groups'

class Groups(Table):
  def __init__(self):
    # TODO убрать settings в MongoManager
    settings = {
      'host': 'localhost', 
      'port': 27017
    }
    self.mongo = MongoManager(settings, 'crud')
    self.groups_collection = self.mongo.collection(collection_name)


  def __del__(self):
    self.mongo.remove_collection(collection_name)


  def fill(self, count):
    fill_groups = self.__generate_groups(count)
    self.groups_collection.insert_many(fill_groups)


  def read_all(self):
    for group in self.groups_collection.find({}, {'_id': 0}):
      pprint.pprint(group)


  def read(self, filter):
    group = self.groups_collection.find_one(filter, {'_id': 0})
    pprint.pprint(group)


  def clear(self):
    self.groups_collection.delete_many({})

  
  def update(self, filter, new_value):
    self.groups_collection.update_one(filter, new_value)


  def __generate_groups(self, count):
    groups = []
    for i in range(count):
      group = {
        'name': f'БСБО-0{i+1}-19',
        'course': 4
      }
      groups.append(group)
    return groups