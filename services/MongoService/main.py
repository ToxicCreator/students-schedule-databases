# app/main.py

from fastapi import FastAPI
import os
import uvicorn
app = FastAPI()


@app.get('/')
async def index():
    return {"message": "Mongo"}

@app.post('/course_info')
async def course_info_by_id(courses_id: list):
    courses = dict()
    for course in courses_id:
        course_info = self.{database_name}.Courses.find_one(filter, {'id': course})
        courses[courses_id] = course_info

    return courses

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9001)