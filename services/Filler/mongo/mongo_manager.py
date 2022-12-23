from pymongo import MongoClient
from singleton import MetaSingleton


# docker run -d --name mongo-cnt -p 27017:27017 mongo
class MongoManager(metaclass=MetaSingleton):

    def __init__(self, host, port, db_name):
        client = MongoClient(host=host, port=port)
        self.db = client[db_name]

    def collection(self, collection_name):
        return self.db[collection_name]

    def remove_collection(self, collection_name):
        self.collection(collection_name).drop()

    def get_collection_names(self):
        return self.db.list_collection_names()