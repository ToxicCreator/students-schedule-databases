from fastapi import FastAPI
import psycopg2
import uvicorn
import os
from pydantic import BaseModel


app = FastAPI()
connection = None
cursor = None


def create_connection():
    settings = parse_data('settings.json')
    connection = psycopg2.connect(
        database = "postgres",
        user = settings["postgresql"]["login"],
        password = settings["postgresql"]["password"],
        host=settings["host"],
        port = settings["postgresql"]["port"]
    )
    cursor = connection.cursor()


def execute_and_commit(query: str) -> None:
    cursor.execute(query)
    connection.commit()
    return cursor.fetchall()


@app.get('/')
async def index():
    return {
        "PostgreSQL": {
            "/percentage-of-visits": {}
        }
    }


class PercentageOfVisitsParams(BaseModel):
    lessons_id: list[int]
    start: str
    end: str


@app.post('/percentage-of-visits')
async def index(body: PercentageOfVisitsParams):
    query = f'''
        SELECT 
            v.student_id, 
            (count(*) FILTER (WHERE v.visited = TRUE))::float / count(*) * 100 
                as percentage_of_visits
        FROM schedule sch
            JOIN visits v ON sch.id = v.schedule_id
            JOIN lessons ls ON sch.lesson_id = ls.id
        WHERE ls.description_id IN {body.lessons_id}
            AND v.date BETWEEN {body.start} AND {body.end}
        GROUP BY v.student_id
        ORDER BY percentage_of_visits LIMIT 10;
    '''
    query = 'SELECT * FROM visits;'
    return execute_and_commit(query)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.getenv('POSTGRES_PORT'))