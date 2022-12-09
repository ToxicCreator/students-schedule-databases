import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from psql_manager import PsqlManager


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
    return execute_and_commit(query)

@app.post('/lessons_data_by_semester')
async def lessons_data_by_semester(semester: int, year: int):
    if semester not in [1, 2]:
        return

    if semester == 1:
        start_date = f'{year}-09-01'
        finish_date = f'{year}-12-31'

    if semester == 2:
        start_date = f'{year+1}-01-01'
        finish_date = f'{year}-07-1'

    query = f'''
    SELECT les.id, sch.course_id, sch.group_id FROM schedule sch 
    WHERE sch.date BETWEEN {start_date} AND {finish_date} 
    JOIN groups gr ON gr.id = sch.group_id
    JOIN lessons les ON les.id = sch.lessons_id
    '''

    self.psql.execute_and_commit(query)
    return self.psql.cursor.fetchall()



if __name__ == "__main__":
    port = int(os.getenv('POSTGRES_PORT', 5050))
    uvicorn.run(app, host="0.0.0.0", port=port)