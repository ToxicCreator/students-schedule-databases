
import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from first_request import makeFirstRequest
from SecondRequestAnswer import SecondRequestAnswer



app = FastAPI()


@app.get('/')
async def index():
    return {
        "/make-first-request": {
            "start_date": "Начало периода обучения",
            "end_date": "Конец периода обучения",
            "term": "Заданный термин или фраза"
        },
        "/make-second-request": {},
        "/make-third-request": {}
    }


@app.get('/make-first-request')
def makeFirstRequest(start: str, end: str, term: str):
    return makeFirstRequest(start, end, term)


@app.get('/make-second-request')
def makeSecondRequest(semester: int, year: int):
    lessons_id, courses_id, groups_id = get_data_by_semester(semester, year)
    student_count = get_students_count_by_groups_is(groups_id)
    courses_info = get_courses_info(courses_id)
    answer = []
    for i in range(len(lessons_id)):
        answer.append(SecondRequestAnswer(lessons_id[i], courses_info[i], student_count[i]))

    return json.dumps(answer.__dict__)

@app.get('/make-third-request')
def makeThirdRequest():
    pass


if __name__ == "__main__":
    port = int(os.getenv('MAIN_HUB_PORT', 9000))
    uvicorn.run(app, host="0.0.0.0", port=port)
