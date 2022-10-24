from pymongo import MongoClient;


class MongoManager():
  def __new__(self):
    if not hasattr(self, 'instance'):
      self.instance = super(MongoManager, self).__new__(self)
    return self.instance


  def __init__(self, settings, db_name):
    client = MongoClient(
      settings['host'], 
      settings['port']
    )
    self.db = client[db_name]


  def collection(self, collection_name):
    return self.db[collection_name]


  def remove_collection(self, collection_name):
    self.collection(collection_name).drop()


  def get_collection_names(self):
    return self.db.list_collection_names()