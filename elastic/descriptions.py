import os
from re import search
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import json
from table import Table
from elasticsearch_dsl import Document
from elastic.elastic_manager import ElasticManager


class Descriptions(Table):
  TABLE_NAME = 'description'
  INDEX_NAME = 'lessons'

  def __init__(self, clear=False):
    self.manager = ElasticManager()
    if clear:
      self.manager.delete_index(self.INDEX_NAME)
    self.lessons_index = self.manager.create_index(
      self.INDEX_NAME
    )


  def insert(self, type, description, tag, lesson_id):
    return self.manager.create_document(
      self.INDEX_NAME,
      {
        'type': type, 
        'description': description, 
        'tag': tag, 
        'lessonId': lesson_id
      }
    )


  def read(self, search):
    return self.manager.read_query(
      self.INDEX_NAME, 
      search
    )


  def update(self, query_map, new_value):
    documents = self.manager.read_query(
      self.INDEX_NAME, 
      query_map
    )
    for hit in documents:
      id = hit.meta.id
      doc_type = hit.meta.doc_type
      result = self.manager.update(
        index=self.INDEX_NAME, 
        id=id, 
        doc_type=doc_type,
        doc=new_value
      )



  def fill(self):
    with open('./elastic/data.json', encoding='utf-8') as file:
      data = json.load(file)
    for doc in data['docs']:
      response = self.insert(doc)
      print(f"\n{response['result']}")


  def print_all(self):
    docs = self.manager.read_index_documents(self.INDEX_NAME)
    for hit in docs:
      print('------------------------')
      print('Name:', hit.Name)
      print('Type:', hit.Type)
      print('Content:', hit.Content)


  def print(self, search):
    for hit in self.read(search):
      print('------------------------')
      print('Name:', hit.Name)
      print('Type:', hit.Type)
      print('Content:', hit.Content)


  def clear(self):
    return super().clear()


  def delete(self, query_map):
    self.manager.delete(self.INDEX_NAME, query_map)