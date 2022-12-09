import os
import redis

class RedisManager():

    def __init__(self):
        self.__make_connection()


    def check_connection(self):
        try:
            self.__database.ping()
            return True
        except:
            return False


    def __make_connection(self):
        self.__database = redis.Redis(
            host=os.getenv("redis_host"),
            port=os.getenv("redis_port"),
            db=0,
            charset='UTF-8',
            decode_responses=True
        )


    def retry_connection(self):
        self.__make_connection()
        return self.check_connection()
