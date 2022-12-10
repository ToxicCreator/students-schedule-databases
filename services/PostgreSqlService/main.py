from fastapi import FastAPI
import os
import uvicorn
from fastapi import FastAPI
from psql_manager import PsqlManager
import psycopg2
import time

time.sleep(5)
app = FastAPI()
connection = psycopg2.connect(
            database=os.getenv('POSTGRES_DBASE_NAME'),
            user=os.getenv('POSTGRES_DBASE_LOGIN'),
            password=os.getenv('POSTGRES_DBASE_PASSWORD'),
            host=os.getenv('POSTGRES_DBASE_IP'),
            port=os.getenv('POSTGRES_PORT_FIRST')
        )
cursor = connection.cursor()
manager = PsqlManager()

@app.get('/')
async def index():
    return {"message": "PostgreSQL"}

@app.get('/select')
async def select():
    query = "SELECT 1;"
    cursor.execute(query)
    connection.commit()
    return cursor.fetchone()



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9005)