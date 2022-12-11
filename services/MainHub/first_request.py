import os
import requests
import json

ELASTIC_SERVICE_IP = os.getenv('ELASTIC_SERVICE_IP')
ELASTIC_SERVICE_PORT = os.getenv('ELASTIC_SERVICE_PORT')
elastic_ip = f'http://{ELASTIC_SERVICE_IP}:{ELASTIC_SERVICE_PORT}/'

POSTGRES_SERVICE_IP = os.getenv('POSTGRES_SERVICE_IP')
POSTGRES_SERVICE_PORT = os.getenv('POSTGRES_SERVICE_PORT')
postgres_url = f'http://{POSTGRES_SERVICE_IP}:{POSTGRES_SERVICE_PORT}/'

REDIS_SERVICE_IP = os.getenv('REDIS_SERVICE_IP')
REDIS_SERVICE_PORT = os.getenv('REDIS_SERVICE_PORT')
redis_url = f'http://{REDIS_SERVICE_IP}:{REDIS_SERVICE_PORT}/'


def makeFirstRequest(start: str, end: str, term: str) -> dict:
    lessons_id = get_lessons_id_by_description(term)
    students_visits = get_percentage_of_visits(
        lessons_id=lessons_id,
        start=start,
        end=end
    ).json()
    students_id = [student[0] for student in students_visits]
    students = get_students(students_id)
    for i, dict_ in enumerate(students):
        for j in range(len(students_visits)):
            if students_visits[j][0] == dict_["key"]:
                students[i]["percent_of_attendance"] = students_visits[j][1]
    result_dict = {
        'date_start': start,
        'date_end': end,
        'term': term,
        "students": students
    }
    return result_dict


def get_lessons_id_by_description(term: str) -> dict:
    url = elastic_ip + 'description'
    result = requests.get(
        url=url,
        params={
            'term': term
        }
    )
    return result.json()


def get_percentage_of_visits(lessons_id, start, end) -> requests.Response:
    url = postgres_url + 'percentage-of-visits'
    postgres_body = {
        'lessons_id': lessons_id,
        'start': start,
        'end': end
    }
    res = requests.post(url=url, json=postgres_body)
    return res


def get_students(students_id):
    url = redis_url + 'students'
    students_dict = {
        "students_id": students_id
    }
    obj = requests.post(url=url, json=students_dict).json()
    return obj
