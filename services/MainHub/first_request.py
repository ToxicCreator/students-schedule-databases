import os
import requests
import itertools

ELASTIC_SERVICE_IP = os.getenv('ELASTIC_SERVICE_IP')
ELASTIC_SERVICE_PORT = os.getenv('ELASTIC_SERVICE_PORT')
elastic_ip = f'http://{ELASTIC_SERVICE_IP}:{ELASTIC_SERVICE_PORT}/'

POSTGRES_SERVICE_IP = os.getenv('POSTGRES_SERVICE_IP')
POSTGRES_SERVICE_PORT = os.getenv('POSTGRES_SERVICE_PORT')
postgres_url = f'http://{POSTGRES_SERVICE_IP}:{POSTGRES_SERVICE_PORT}/'

REDIS_SERVICE_IP = os.getenv('REDIS_SERVICE_IP')
REDIS_SERVICE_PORT = os.getenv('REDIS_SERVICE_PORT')
redis_url = f'http://{REDIS_SERVICE_IP}:{REDIS_SERVICE_PORT}/'

NEO4J_SERVICE_IP = os.getenv('NEO4J_SERVICE_IP')
NEO4J_SERVICE_PORT = os.getenv('NEO4J_SERVICE_PORT')
neo4j_url = f'http://{NEO4J_SERVICE_IP}:{NEO4J_SERVICE_PORT}/'


def makeFirstRequest(start: str, end: str, term: str) -> dict:
    description_id = get_description_id(term)
    lessons_id = get_lessons_id_by(description_id)
    visits_id = get_visits_id_by(lessons_id)
    students_visits = get_percentage_of_visits_by_date(
        date_start=start,
        date_end=end,
        visits_id=visits_id
    )
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

def get_description_id(term: str) -> dict:
    url = elastic_ip + 'description'
    result = requests.get(
        url=url,
        params={
            'term': term
        }
    )
    return result.json()

def get_lessons_id_by(descriptions_id):
    url = postgres_url + 'lessons-by-desscriptions-id'
    query_body = {
        "descriptions_id": descriptions_id
    }
    return requests.post(url=url, json=query_body).json()

def get_visits_id_by(lessons_id):
    url = neo4j_url + 'visits-by-lessons-id'
    query_body = {
        "lessons_id": list(itertools.chain(*lessons_id))
    }
    return requests.post(url=url, json=query_body).json()

def get_percentage_of_visits_by_date(date_start, date_end, visits_id):
    url = postgres_url + 'percentage-of-visits-by-date'
    query_body = {
        "visits_id": list(itertools.chain(*visits_id)),
        "start": date_start,
        "end": date_end
    }
    return requests.post(url=url, json=query_body).json()

def get_students(students_id):
    url = redis_url + 'students'
    query_body = {
        "students_id": students_id
    }
    obj = requests.post(url=url, json=query_body).json()
    return obj
