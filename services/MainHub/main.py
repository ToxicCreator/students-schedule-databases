
import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import requests


app = FastAPI()
load_dotenv()

ELASTIC_IP = os.getenv('ELASTIC_IP')
ELASTIC_PORT = os.getenv('ELASTIC_PORT')
elastic_ip = f'https://{ELASTIC_IP}:{ELASTIC_PORT}/'

POSTGRES_IP = os.getenv('POSTGRES_IP')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
postgres_url = f'https://{POSTGRES_IP}:{POSTGRES_PORT}/'

REDIS_IP = os.getenv('REDIS_IP')
REDIS_PORT = os.getenv('REDIS_PORT')
redis_url = f'https://{REDIS_IP}:{REDIS_PORT}/'


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


@app.get('/make-second-request')
def makeSecondRequest():
    pass


@app.get('/make-third-request')
def makeThirdRequest():
    pass


def get_lessons_id_by_description(term: str):
    url = elastic_ip + 'description'
    return requests.get(
        url=url, 
        params={
            'term': term
        }
    )


def get_percentage_of_visits(lessons_id, start, end):
    url = postgres_url + 'percentage-of-visits'
    postgres_body = {
        'lessons_id': lessons_id,
        'start': start,
        'end': end
    }
    return requests.post(url=url, json=postgres_body)


def get_students(students_id):
    url = redis_url + 'students'
    return requests.post(url=url, json={
        "students_id": students_id
    })


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.getenv('MAIN_HUB_PORT'))
