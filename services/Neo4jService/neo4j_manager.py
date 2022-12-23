import os
import neo4j
from neo4j import GraphDatabase


class Neo4jManager:

    def __init__(self):
        self.__session: neo4j.Session = self.__make_connection()

    def check_connection(self) -> bool:
        try:
            self.__session.run("Match () return 1 Limit 1")
        except (Exception,):
            return False
        return True

    @staticmethod
    def __make_connection() -> neo4j.Session:
        session = GraphDatabase.driver(
            uri="bolt://{0}:{1}".format(os.getenv('NEO4J_DBASE_IP'), int(os.getenv('NEO4J_DBASE_PORT_SECOND'))),
            auth=(str(os.getenv('NEO4J_DBASE_LOGIN')), str(os.getenv('NEO4J_DBASE_PASSWORD'))),
            max_connection_pool_size=100000).session()
        return session

    def retry_connection(self):
        self.__make_connection()
        return self.check_connection()
