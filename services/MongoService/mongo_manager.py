import os
from pymongo import MongoClient


class MongoManager():

    def __init__(self, db_name):
        self.__client = self.__make_connection()
        self.db = self.__client[db_name]


    def check_connection(self):
        try:
            self.__client.server_info()
            return True
        except:
            return False


    def __make_connection(self):
        return MongoClient(
            host=os.getenv("host"),
            port=os.getenv("port")
        )


    def retry_connection(self):
        self.__client = self.__make_connection()
        return self.check_connection()


    def collection(self, collection_name):
        return self.db[collection_name]
