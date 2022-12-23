from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import time
from typing import List
from neo4j_manager import Neo4jManager



app = FastAPI()
time.sleep(10)
manager = Neo4jManager()

@app.get('/')
async def index():
    return {"message": "Neo4j"}

class VisitsQueryBody(BaseModel):
    lessons_id: List[str]

@app.get('/visits-by-lessons-id')
async def visits_by_lessons_id(body: VisitsQueryBody):
    query = f'''
        MATCH(v:visit) WHERE v.name in [{"', '".join(body.lessons_id)}] return v
    '''
    return list(manager.execute_query(query))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9002)
