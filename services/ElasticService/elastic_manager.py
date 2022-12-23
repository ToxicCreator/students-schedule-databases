import os
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index, Q, Search
from typing import Dict


class ElasticManager:

    def __init__(self):
        self.connect()

    def check_connection(self) -> bool:
        return self.__client.ping()

    def connect(self) -> None:
        elastic_ip = os.getenv("ELASTIC_DBASE_IP")
        elastic_port = os.getenv("ELASTIC_DBASE_PORT")
        self.__client = Elasticsearch('http://root:root@{0}:{1}'.format(elastic_ip, elastic_port))

    def retry_connection(self) -> bool:
        self.connect()
        return self.check_connection()

    def read_query(self, index, query_map: Dict[str, str]):
        search = Search(using=self.__client, index=index)
        for key, value in query_map.items():
            search.query = Q(
                'bool',
                should=[Q('match', **{key: value})]
            )
        search.query(
            minimum_should_match=len(query_map.values())
        )
        return search.execute()
