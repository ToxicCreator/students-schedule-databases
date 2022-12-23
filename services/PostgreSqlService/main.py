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


@app.get('/')
async def index():
    return {
        "PostgreSQL": {
            "/percentage-of-visits": {}
        }
    }

class LessonsQueryBody(BaseModel):
    descriptions_id: List[str]

@app.post('/lessons-by-desscriptions-id')
async def lessons_by_desscriptions_id(body: LessonsQueryBody):
    query = f'''
        SELECT id 
        FROM lessons 
        WHERE description_id IN ('{"', '".join(body.descriptions_id)}');
    '''
    return manager.execute_and_commit(query)

class PercentageQueryBody(BaseModel):
    visits_id: List[int]
    start: str
    end: str

@app.post('/percentage-of-visits-by-date')
async def percentage_of_visits_by_date(body: PercentageQueryBody):
    query = f'''
        SELECT 
            student_id, 
            (count(*) FILTER (WHERE visited = TRUE))::float / count(*) * 100 
                as percentage_of_visits
        FROM visits
        WHERE id IN ({", ".join([str(item) for item in body.visits_id])})
            AND date BETWEEN '{body.start}' AND '{body.end}'
        GROUP BY student_id
        ORDER BY percentage_of_visits LIMIT 10;
    '''
    return manager.execute_and_commit(query)

if __name__ == "__main__":
    port = int(os.getenv('POSTGRES_SERVICE_PORT', 5050))
    uvicorn.run(app, host="0.0.0.0", port=port)
