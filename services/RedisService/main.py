import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from redis_manager import RedisManager
import redis
import os

redis_db = redis.Redis(
            host=str(os.getenv('REDIS_DBASE_IP')),
            port=os.getenv('REDIS_DBASE_PORT'),
            db=int(os.getenv('REDIS_DB')),
            charset=str(os.getenv('REDIS_CHARSET')),
            decode_responses=True
        )
app = FastAPI()
manager = RedisManager()

@app.get('/')
async def index():
    return {"message": "Redis"}


class StudentsParams(BaseModel):
    students: list[str]

@app.post('/students')
async def students(body: StudentsParams) -> list:
    requested_students = []
    for key in body.students:
        requested_students.append(manager.read(key))
    return requested_students


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9003)