from pymongo import MongoClient
from singleton import MetaSingleton

<<<<<<< Updated upstream
# docker run -d --name mongo-cnt -p 27017:27017 mongo
class MongoManager():
    def __new__(self, host, port, db_name):
        if not hasattr(self, 'instance'):
            self.instance = super(MongoManager, self).__new__(self)
      return self.instance


    def __init__(self, host, port, db_name):
        client = MongoClient(host = host, port = port)
        self.db = client[db_name]
=======
>>>>>>> Stashed changes

# docker run -d --name mongo-cnt -p 27017:27017 mongo
class MongoManager(metaclass = MetaSingleton):

<<<<<<< Updated upstream
    def collection(self, collection_name):
        return self.db[collection_name]


    def remove_collection(self, collection_name):
        self.collection(collection_name).drop()
=======
    def __init__(self, db_name):
        client = MongoClient("mongodb://localhost:27017/")
        self.db = client[db_name]

    def collection(self, collection_name):
        return self.db[collection_name]
>>>>>>> Stashed changes

    def remove_collection(self, collection_name):
        self.collection(collection_name).drop()

    def get_collection_names(self):
<<<<<<< Updated upstream
        return self.db.list_collection_names()
=======
        return self.db.list_collection_names()
>>>>>>> Stashed changes
