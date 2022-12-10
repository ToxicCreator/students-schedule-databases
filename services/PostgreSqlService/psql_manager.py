import os
import psycopg2

database = "postgres"

class PsqlManager():

    def __init__(self):
        self.__make_connection()


    def check_connection(self):
        try:
            self.__cursor.execute('SELECT 1')
            return True
        except:
            return False


    def __make_connection(self):
        try:
            self.__connection = psycopg2.connect(
                database=database,
                host=os.getenv("host"),
                port=os.getenv("port"),
                user=os.getenv("login"),
                password=os.getenv("password")
            )
            self.__cursor = self.__connection.cursor()
            return True
        except:
            return False


    def retry_connection(self):
        return self.__make_connection()

    def __del__(self):
        self.__connection.close()

    def execute_and_commit(self, query: str):
        self.__cursor.execute(query)
        self.__connection.commit()
        return self.__cursor.fetchall()
