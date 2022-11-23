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

<<<<<<< Updated upstream
class Institutes():
    def __init__(self, clear=False):
        settings = parse_data('../settings.json')
        self.mongo = MongoManager(settings["host"], settings["mongo"]["port"], database_name)
        self.graph = Graph()
        if clear: self.mongo.remove_collection(collection_name)
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
        
=======

class Institutes:
    def __init__(self, clear = False):
        self.mongo = MongoManager(database_name)
        self.graph = Graph()
        if clear:
            self.mongo.remove_collection(collection_name)
        self.collection = self.mongo.collection(collection_name)

    def fill(self, path):
        institutes = parse_data(path)

        for institute in institutes:
            self.graph.create_institute_node(institute['name'])
            for department in institute['departments']:
                self.graph.create_department_node(department['name'], institute['name'])
                for speciality in department['specialities']:
                    code = speciality['code']
                    name = speciality['name']
                    self.graph.create_speciality_node(code, name, department['name'])

>>>>>>> Stashed changes
        if isinstance(institutes, list):
            self.collection.insert_many(institutes)
        else:
            self.collection.insert_one(institutes)

<<<<<<< Updated upstream
        
        # courses = self.__parse_data('mongo\courses.json')
        # cut = random.randint(1, len(courses))
        # self.collection.update_many(
        #     {},
        #     [{ '$set': { 'departments.specialities.courses': courses[:cut] } }]
        # )


=======
        # courses = self.__parse_data('mongo\courses.json')
        # cut = random.randint(1, len(courses))
        # self.collection.update_many(
        #   {},
        #   [{ '$set': { 'departments.specialities.courses': courses[:cut] } }]
        # )

>>>>>>> Stashed changes
    def get_specialities_codes(self):
        codes = []
        institutes = self.collection.find({}, {
            'departments.specialities': 1
        })
        for institute in institutes:
            for department in institute['departments']:
                for speciality in department['specialities']:
                    codes.append(speciality['code'])
        return codes

<<<<<<< Updated upstream

    # def get_courses_id(self):
    #     courses_id = []
    #     institutes = self.collection.find({}, {
    #         'departments.specialities.courses': 1
    #     })
    #     for institute in institutes:
    #         for department in institute['departments']:
    #             for speciality in department['specialities']:
    #                 for course in speciality['courses']:
    #                     courses_id.append(course['_id'])
    #     return courses_id

=======
    # def get_courses_id(self):
    #   courses_id = []
    #   institutes = self.collection.find({}, {
    #     'departments.specialities.courses': 1
    #   })
    #   for institute in institutes:
    #     for department in institute['departments']:
    #       for speciality in department['specialities']:
    #         for course in speciality['courses']:
    #           courses_id.append(course['_id'])
    #   return courses_id
>>>>>>> Stashed changes

    def read(self, filter):
        return self.collection.find(filter, {'_id': 0})

<<<<<<< Updated upstream

    def clear(self):
        self.collection.delete_many({})


=======
    def clear(self):
        self.collection.delete_many({})

>>>>>>> Stashed changes
    def update(self, filter, new_value):
        self.collection.update_one(filter, new_value)
