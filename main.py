import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

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
def makeThirdRequest(group_id):
    lessons = get_group_lessons_by_id(group_id)
    filtered_lessons = get_filtered_lessons_by_department(group_id, lessons)
    studying_info = get_studying_info(group_id, filtered_lessons)
    students_info = get_students_info(student_ids)
    group_info = get_group_info_by_id(group_id)
    courses_info = get_courses_info(course_ids)
    return generate_third_request_response_json()



def get_lessons_id_by_description(term: str):
    url = elastic_ip + 'description'
    return requests.get(url, params={
        'term': term
    })


def get_percentage_of_visits(lessons_id, start, end):
    url = postgres_url + 'percentage-of-visits'
    postgres_body = {
        'lessons_id': lessons_id,
        'start': start,
        'end': end
    }
    return requests.post(url, json=postgres_body)


def get_students(students_id):
    url = redis_url + 'students'
    return requests.post(url, json={
        "students_id": students_id
    })

def get_group_lessons_by_id(group_id):
    url = postgres_url + 'group-lessons-by-id'
    return requests.get(url, params={
        'group_id': group_id
    })

def get_filtered_lessons_by_department(group_id, lessons):
    url = neo4j_url + 'filtered-lessons_by-department'
    postgres_body = {
        'lessons': lessons,
        'group_id': group_id
    }
    return requests.post(url, json=postgres_body)

def get_studying_info(group_id, filtered_lessons):
    pass

def get_students_info(student_ids):
    pass

def get_group_info_by_id(group_id):
    pass

def get_courses_info(course_ids):
    pass


if __name__ == "__main__":
    port = int(os.getenv('MAIN_HUB_PORT', 9000))
    uvicorn.run(app, host="0.0.0.0", port=port)
