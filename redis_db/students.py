import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from table import Table
import random
import redis
from neo4j_db.graph import Graph

# docker run -d --name redis-cnt -p 6379:6379 redis
class Students(Table):
    __shifrs = set()

    def __init__(self, host, port, clear=False):
        self.redis_db = redis.Redis(
            host=host,
            port=port,
            db=0,
            charset='UTF-8',
            decode_responses=True
        )
        self.graph = Graph()
        if clear:
            self.clear()


    def get_shifrs(self):
        return self.__shifrs


    def read(self, key):
        return self.redis_db.hgetall(key)

    def insert(self, name, surname, group_name):
        key = self.__get_shifr()
        self.redis_db.hset(key, 'name', name)
        self.redis_db.hset(key, 'surname', surname)
        self.redis_db.hset(key, 'groupID', group_name)
        # self.graph.create_student_node(key, name, group_name)
        return key


    def update(self, key, new_value):
        self.redis_db.hmset(key, new_value)


    def clear(self):
        keys = self.redis_db.keys()
        for key in keys:
            self.redis_db.delete(key)


    def __get_shifr(self):
        shifr = [random.choice('АБВГД') for _ in range(3)]
        shifr.append('-')
        shifr += [random.choice('0123456789') for _ in range(5)]
        shifr = ''.join(shifr)
        if shifr in self.__shifrs:
            return self.__get_shifr()
        self.__shifrs.add(shifr)
        return shifr


    def get_by_group(self, group_name):
        group = []
        keys = self.redis_db.keys()
        for key in keys:
            student = self.read(key)
            if student['group_name'] == group_name:
                group.append(key)
        return group


    def print_all(self):
        keys = self.redis_db.keys('*')
        for key in keys:
            self.print(key)


    def print(self, key):
        student = self.read(key)
        print(key, student)


if __name__ == "__main__":
    pass

