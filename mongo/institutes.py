import os
import sys
from table import Table
from mongo.mongo_manager import MongoManager
from neo4j_db.graph import Graph
from utils import parse_data
import time

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

database_name = 'prac_3'
collection_name = 'institutes'

class Institutes:
    institutes: dict
    def __init__(self, clear=False):
        settings = parse_data('settings.json')
        self.mongo = MongoManager(settings["host"], settings["mongodb"]["port"], database_name)
        self.graph = Graph()
        time.sleep(10)
        if clear:
            self.mongo.remove_collection(collection_name)
        self.collection = self.mongo.collection(collection_name)

    def parse_institutes(self, path):
        self.institutes = parse_data(path)

    def fill(self):
        if isinstance(self.institutes, list):
            self.collection.insert_many(self.institutes)
        else:
            self.collection.insert_one(self.institutes)

    def make_neo4j_shortcuts(self):
        for institute in self.institutes:
            for department in institute['Departments']:
                self.graph.create_department_node(name=department['Name'])
                for speciality in department['Specialities']:
                    self.graph.create_speciality_node(name=speciality['Name'],
                                                      code=speciality['Code'],
                                                      department_name=department['Name'])
                for course in department['Courses']:
                    self.graph.create_course_node(name=course['Name'],
                                                  department_name=department['Name'])

    def get_specialities_codes(self):
        codes = []
        institutes = self.collection.find({})

        for institute in institutes:
            for department in institute['Departments']:
                for speciality in department['Specialities']:
                    codes.append(speciality['Code'])
        return codes

    def get_courses_ids(self):
        courses = []
        institutes = self.collection.find({})

        for institute in institutes:
            for department in institute['Departments']:
                for course in department['Courses']:
                    courses.append(course['ID'])
                    
        return courses

    def get_departments_courses(self):
        dep_courses = {}
        institutes = self.collection.find({})

        for institute in institutes:
            for department in institute['Departments']:
                dep_courses[department["Code"]] = []
                for course in department['Courses']:
                    dep_courses[department["Code"]].append(course["ID"])
        return dep_courses

    def get_departments_specialities(self):
        deps_specialities = {}
        institutes = self.collection.find({})
        for institute in institutes:
            for department in institute['Departments']:
                deps_specialities[department["Code"]] = []
                for speciality in department['Specialities']:
                    deps_specialities[department["Code"]].append(speciality["Code"])
        return deps_specialities

    def get_course_names_by_ids(self, course_ids):
        course_names = []
        for institute in self.institutes:
            for department in institute['Departments']:
                for course in department['Courses']:
                    if course['ID'] in course_ids:
                        course_names.append(course['Name'])
        return course_names



    def read(self, filter):
        return self.collection.find(filter, {'_id': 0})

    def clear(self):
        self.collection.delete_many({})

    def update(self, filter, new_value):
        self.collection.update_one(filter, new_value)
