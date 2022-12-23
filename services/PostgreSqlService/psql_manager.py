import os
import psycopg2
from typing import List


class PsqlManager:

    def __init__(self):
        self.connect()

    def check_connection(self):
        try:
            self.cursor.execute('SELECT 1')
        except psycopg2.OperationalError:
            return False
        return True

    def connect(self) -> bool:
        try:
            self.__connection = psycopg2.connect(
                database=os.getenv('POSTGRES_DBASE_NAME'),
                user=os.getenv('POSTGRES_DBASE_LOGIN'),
                password=os.getenv('POSTGRES_DBASE_PASSWORD'),
                host=os.getenv('POSTGRES_DBASE_IP'),
                port=os.getenv('POSTGRES_PORT_FIRST')
            )
            self.cursor = self.__connection.cursor()
        except psycopg2.OperationalError:
            return False
        return True

    def retry_connection(self):
        return self.connect()

    def __del__(self):
        self.__connection.close()

    def execute_and_commit(self, query: str) -> List[tuple]:
        self.cursor.execute(query)
        self.__connection.commit()
        return self.cursor.fetchall()
