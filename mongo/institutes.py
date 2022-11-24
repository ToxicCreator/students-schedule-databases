import os
import sys
from table import Table
from mongo.mongo_manager import MongoManager
from neo4j_db.graph import Graph
from utils import parse_data

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

database_name = 'prac_3'
collection_name = 'institutes'


class Institutes:
    def __init__(self, clear = False):
        settings = parse_data('settings.json')
        self.mongo = MongoManager(settings["host"], settings["mongodb"]["port"], database_name)
        self.graph = Graph()
        if clear:
            self.mongo.remove_collection(collection_name)
        self.collection = self.mongo.collection(collection_name)

    def fill(self, path):
        institutes = parse_data(path)

        # for institute in institutes:
        #     self.graph.create_institute_node(institute['name'])
        #     for department in institute['departments']:
        #         self.graph.create_department_node(department['name'], institute['name'])
        #         for speciality in department['specialities']:
        #             code = speciality['code']
        #             name = speciality['name']
        #             self.graph.create_speciality_node(code, name, department['name'])

        if isinstance(institutes, list):
            self.collection.insert_many(institutes)
        else:
            self.collection.insert_one(institutes)

        # courses = self.__parse_data('mongo\courses.json')
        # cut = random.randint(1, len(courses))
        # self.collection.update_many(
        #     {},
        #     [{ '$set': { 'departments.specialities.courses': courses[:cut] } }]
        # )

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


    def read(self, filter):
        return self.collection.find(filter, {'_id': 0})

    def clear(self):
        self.collection.delete_many({})

    def update(self, filter, new_value):
        self.collection.update_one(filter, new_value)
