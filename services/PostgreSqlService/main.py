import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from psql_manager import PsqlManager
import time
from typing import List


app = FastAPI()
time.sleep(5)
manager = PsqlManager()
manager.connect()


@app.get('/')
async def index():
    return {
        "PostgreSQL": {
            "/percentage-of-visits": {}
        }
    }


class PercentageOfVisitsParams(BaseModel):
    lessons_id: List[str]
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
            JOIN visits v ON sch.id = v.shedule_id
            JOIN lessons ls ON sch.lesson_id = ls.id
        WHERE ls.description_id IN ('{"', '".join(body.lessons_id)}')
            AND v.date BETWEEN '{body.start}' AND '{body.end}'
        GROUP BY v.student_id
        ORDER BY percentage_of_visits LIMIT 10;
    '''
    return manager.execute_and_commit(query)


if __name__ == "__main__":
    port = int(os.getenv('POSTGRES_SERVICE_PORT', 5050))
    uvicorn.run(app, host="0.0.0.0", port=port)
