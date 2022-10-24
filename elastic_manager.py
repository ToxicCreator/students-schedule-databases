from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


class ElasticManager():
  def __new__(self):
    if not hasattr(self, 'instance'):
      self.instance = super(ElasticManager, self).__new__(self)
    return self.instance


  def __init__(self):
    self.client = Elasticsearch('http://root:root@localhost:9200')
    print("ElasticSearch connected successfully.")


  def read(self, index):
    resp = self.client.search(index="course", query = query)
    resp = Search(using=self.client, index=index)

    if not resp['hits']['hits']:
      print (f"\n{resp}")
        
    for i in range(len(resp["hits"]["hits"])):
      print()
      print(resp["hits"]["hits"][i]["_source"])