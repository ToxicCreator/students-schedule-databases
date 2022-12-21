import os
import pymongo
from pymongo import MongoClient


class MongoManager:

    def __init__(self):
        self.__client: MongoClient = self.__make_connection()
        self.db: MongoClient = self.__client[str(os.getenv('MONGO_DBASE_NAME'))]

    def check_connection(self):
        try:
            self.__client.server_info()
        except (Exception,):
            return False
        return True

    @staticmethod
    def __make_connection() -> MongoClient:
        return MongoClient(
            host=os.getenv("MONGO_DBASE_IP"),
            port=int(os.getenv("MONGO_DBASE_PORT_SECOND"))
        )

    def retry_connection(self) -> bool:
        self.__client = self.__make_connection()
        return self.check_connection()

    def get_collection(self, collection_name: str) -> pymongo.collection.Collection:
        return self.db[collection_name]
