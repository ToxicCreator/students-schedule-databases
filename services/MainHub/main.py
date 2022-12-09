
import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import requests
from SecondRequestAnswer import SecondRequestAnswer



app = FastAPI()
load_dotenv()

ELASTIC_IP = os.getenv('ELASTIC_IP')
ELASTIC_PORT = os.getenv('ELASTIC_PORT')
elastic_url = f'https://{ELASTIC_IP}:{ELASTIC_PORT}/'

POSTGRES_IP = os.getenv('POSTGRES_IP')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
postgres_url = f'https://{POSTGRES_IP}:{POSTGRES_PORT}/'

REDIS_IP = os.getenv('REDIS_IP')
REDIS_PORT = os.getenv('REDIS_PORT')
redis_url = f'https://{REDIS_IP}:{REDIS_PORT}/'

NEO4J_IP = os.getenv('NEO4J_IP')
NEO4J_PORT = os.getenv('NEO4J_PORT')
neo4j_url = f'https://{NEO4J_IP}:{NEO4J_PORT}/'

MONGO_IP = os.getenv('MONGO_IP')
MONGO_PORT = os.getenv('MONGO_PORT')
mongo_url = f'https://{MONGO_IP}:{MONGO_PORT}/'


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
    lessons_id = get_lessons_id_by_description(term)
    (students_id, percentage_of_visits) = get_percentage_of_visits(
        lessons_id,
        start,
        end
    )
    students = get_students(students_id)


def get_data_by_semester(semester: int, year: int):
    url = postgres_url + 'lessons_data_by_semester'
    postgres_body = {
        'semester': semester,
        'year': year
    }
    return requests.post(url, json=postgres_body)


def get_students_count_by_groups_is(groups_id: list):
    url = neo4j_url + 'count_of_students'
    postgres_body = {
        'groups_id': groups_id
    }
    return requests.post(url, json=postgres_body)


def get_courses_info(courses_id: list):
    url = mongo_url + 'course_info'
    postgres_body = {
        'courses_id': courses_id
    }
    return requests.post(url, json=postgres_body)


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


def get_lessons_id_by_description(term: str):
    url = elastic_url + 'description'
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.getenv('MAIN_HUB_PORT'))
