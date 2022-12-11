import os
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index, Q, Search

class ElasticManager:

    def __init__(self):
        self.__make_connection()


    def check_connection(self):
        return self.__client.ping()


    def __make_connection(self):
        elastic_ip = os.getenv("ELASTIC_DBASE_IP")
        elastic_port = os.getenv("ELASTIC_DBASE_PORT")
        self.__client = Elasticsearch('http://root:root@{0}:{1}'.format(os.getenv('ELASTIC_DBASE_IP'),
                                                                      os.getenv('ELASTIC_DBASE_PORT')))



    def retry_connection(self):
        self.__make_connection()
        return self.check_connection()


    def read_query(self, index, query_map: dict[str, str]):
        return self.searh_by_map(index, query_map).execute()


    def searh_by_map(self, index, query_map: dict[str, str]):
        search = Search(using = self.__client, index = index)
        for key, value in query_map.items():
            search.query = Q(
                'bool',
                should = [Q('match', **{key: value})]
            )
        search.query(
            minimum_should_match = len(query_map.values())
        )
        return search
