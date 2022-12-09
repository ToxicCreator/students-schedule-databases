import os
import uvicorn
<<<<<<< HEAD
from fastapi import FastAPI
from pydantic import BaseModel
from psql_manager import PsqlManager

=======
import psycopg2
>>>>>>> 9b54281 (Initial commit)

app = FastAPI()
manager = PsqlManager()

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
async def percentage_of_visits(body: PercentageOfVisitsParams):
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
    return manager.execute_and_commit(query)

@app.get('group-lessons-by-id')
def group_lessons_by_id(group_id):
    pass

if __name__ == "__main__":
    port = int(os.getenv('POSTGRES_PORT', 5050))
    uvicorn.run(app, host="0.0.0.0", port=port)