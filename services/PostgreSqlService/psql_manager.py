import os
import psycopg2

database = "postgres"

class PsqlManager:

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
            print('1')
            self.__connection = psycopg2.connect(
                database=os.getenv('POSTGRES_DBASE_NAME'),
                user=os.getenv('POSTGRES_DBASE_LOGIN'),
                password=os.getenv('POSTGRES_DBASE_PASSWORD'),
                host=os.getenv('POSTGRES_DBASE_IP'),
                port=os.getenv('POSTGRES_PORT_FIRST')
            )
            print('2')
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
