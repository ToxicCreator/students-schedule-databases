from fastapi import FastAPI
import psycopg2
import uvicorn
import os
from utils import parse_data

app = FastAPI()


def qwe():
    settings = parse_data('settings.json')
    connection = psycopg2.connect(
        database = "postgres",
        user = settings["postgresql"]["login"],
        password = settings["postgresql"]["password"],
        host=settings["host"],
        port = settings["postgresql"]["port"]
    )
    cursor = connection.cursor()


    def __del__(self):
        self.connection.close()


    def execute_and_commit(self, query: str) -> None:
        self.cursor.execute(query)
        self.connection.commit()


    self.psql = PsqlManager(settings["host"], settings["postgresql"]["port"], 
                            settings["postgresql"]["login"], settings["postgresql"]["password"])


@app.get('/')
async def index():
    return {
        "PostgreSQL": {
            "/percentage-of-visits": {}
        }
    }


@app.get('/percentage-of-visits')
async def index():
    return {"message": "PostgreSQL"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.getenv('POSTGRES_PORT'))