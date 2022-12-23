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
    lessons_id: List[int]


@app.post('/visits-by-lessons-id')
async def visits_by_lessons_id(body: VisitsQueryBody):
    body.lessons_id = map(str, body.lessons_id)
    listing = ", ".join(body.lessons_id)
    query = f'''
        MATCH (v:visit)-[:refers_to]->(l:lesson) WHERE l.Id in [{listing}] RETURN v.id
    '''
    result = manager.execute_query(query)
    return list(result)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9002)
