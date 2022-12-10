from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from neo4j_manager import Neo4jManager

app = FastAPI()
manager = Neo4jManager()

class GroupLessonsParmas(BaseModel):
    lessons: list[int]
    group_id: str

@app.get('/')
async def index():
    return {"message": "Neo4j"}

@app.post('/filtered-lessons-by-department')
async def filtered_lessons_by_department(body: GroupLessonsParmas):
    if manager.check_connection() != True:
            if manager.retry_connection() != True:
                return {}
        return __get_filtered_lessons_by_department(body)

def __get_filtered_lessons_by_department(body):
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9002)