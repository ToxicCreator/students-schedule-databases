import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from redis_manager import RedisManager
import os
from typing import List

app = FastAPI()
manager = RedisManager()
manager.connect()


@app.get('/')
async def index():
    return {"message": "Redis"}


class StudentsParams(BaseModel):
    students_id: List[str]


@app.post('/students')
async def students(body: StudentsParams) -> List:
    requested_students = []
    manager.print_all()
    for key in body.students_id:
        qq = manager.read(key)
        qq["key"] = key
        requested_students.append(qq)
    return requested_students


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9003)
