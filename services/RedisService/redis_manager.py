import os
import redis
from typing import Union, Awaitable, List


class RedisManager:

    def __init__(self):
        self.connect()

    def check_connection(self) -> bool:
        try:
            self.__database.ping()
        except redis.exceptions.ConnectionError:
            return False
        return True

    def connect(self) -> bool:
        try:
            self.__database = redis.Redis(
                host=os.getenv("REDIS_DBASE_IP", "localhost"),
                port=int(os.getenv("REDIS_DBASE_PORT", 6379)),
                db=0,
                charset='UTF-8',
                decode_responses=True
            )
        except redis.exceptions.ConnectionError:
            return False
        return True

    def retry_connection(self) -> bool:
        self.connect()
        return self.check_connection()

    def read(self, key: str) -> Union[Awaitable[dict], dict]:
        return self.__database.hgetall(key)

    def print_all(self):
        keys = self.__database.keys('*')
        for key in keys:
            print(key)
