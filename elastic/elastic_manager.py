import time

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index, Q, Search

LAG = 0.5

class ElasticManager():
  def __new__(self):
    if not hasattr(self, 'instance'):
      self.__instance__ = super(ElasticManager, self).__new__(self)
    return self.__instance__


  def __init__(self):
    self.__client__ = Elasticsearch('http://root:root@localhost:9200')
    print('ElasticSearch connected successfully.')


  def create_index(self, name):
    index = Index(name, using=self.__client__)
    if not index.exists():
      index.create()
    time.sleep(LAG)
    return index


  def delete_index(self, name):
    index = Index(name, using=self.__client__)
    if not index.exists(): return
    index.delete()
    print(f'Index "{name}" has been deleted.')


  def create_document(self, index, document):
    new_index = self.__client__.index(
      index=index,
      document=document
    )
    time.sleep(LAG)
    return new_index


  def read_index_documents(self, index):
    search = Search().using(self.__client__) \
            .index(index) \
            .execute()
    return search


  def read_query(self, index, query_map: map):
    return self.searh_by_map(index, query_map).execute()


  def update(self, index, id, doc_type, doc):
    updated = self.__client__.update(
      index=index, id=id, doc_type=doc_type, doc=doc
    )
    time.sleep(LAG)
    return updated


  def delete(self, index, query_map: map):
    search = self.searh_by_map(index, query_map)
    return search.delete()


  def searh_by_map(self, index, query_map: map):
    search = Search(using=self.__client__, index=index)
    for key, value in query_map.items():
      search.query = Q(
        'bool', 
        should=[Q('match', **{key:value})]
      )
    search.query(
      minimum_should_match=len(query_map.values())
    )
    return search