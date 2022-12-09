import os
from neo4j import GraphDatabase

class Neo4jManager():

    def __init__(self):
        self.__make_connection()

    def check_connection(self):
        try:
            self.__session.run("Match () return 1 Limit 1")
            return True
        except:
            return False

    def __make_connection(self):
        self.__driver = GraphDatabase.driver(
            uri=f'bolt://{os.getenv("neo4j_host")}:{os.getenv("neo4j_port")}',
            auth=(os.getenv("neo4j_login"), os.getenv("neo4j_password")),
            max_connection_pool_size=100000
        )
        self.__session = self.__driver.session()

    def retry_connection(self):
        self.__make_connection()
        return self.check_connection()
