import os
from re import search
import sys
import json
import time
from table import Table
from elastic.elastic_manager import ElasticManager
from random import randint
from elasticsearch_dsl import Document
from fishtext import FishTextJson
from fishtext.types import TextType, JsonAPIResponse
from utils import parse_data

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

EQUIPMENT = ["компьютер", "проектор", "маркерная доска", "флеш-накопитель", "смарт-токен", "сетевой шкаф", "кликер",
             "набор маркеров", "проекционная доска", "чертежные наборы", "образ виртуальной машины kali linux"]

class Descriptions():
    TABLE_NAME = 'description'
    INDEX_NAME = 'lessons'

    def __init__(self, clear=False):
        settings = parse_data('settings.json')
        self.manager = ElasticManager(settings["host"], settings["elasticsearch"]["port"])
        self.generator_api = FishTextJson(text_type=TextType.Title)
        time.sleep(10)
        if clear:
            self.manager.delete_index(self.INDEX_NAME)
        self.lessons_index = self.manager.create_index(self.INDEX_NAME)

    def insert(self):
        materials = self.get_random_materials()
        equip = Descriptions.get_random_equipment()
        return self.manager.create_document(
            self.INDEX_NAME,
            {
                'equipment': equip,
                'materials': materials
            }
        )['_id']

    def get_random_materials(self):
        titles = self.generator_api.get(10)
        return '. '.join(titles.text.split("\\n\\n"))


    @staticmethod
    def get_random_equipment():
        equipment_ = EQUIPMENT[randint(0, 5):randint(6, 10)]
        return ', '.join(equipment_).rstrip(', ')



    def read(self, search):
        return self.manager.read_query(
            self.INDEX_NAME,
            search
        )

    def update(self, query_map, new_value):
        documents = self.manager.read_query(
            self.INDEX_NAME,
            query_map
        )
        for hit in documents:
            id = hit.meta.id
            doc_type = hit.meta.doc_type
            result = self.manager.update(
                index=self.INDEX_NAME,
                id=id,
                doc_type=doc_type,
                doc=new_value
            )

    def fill(self):
        with open('./elastic/data.json', encoding='utf-8') as file:
            data = json.load(file)
        for doc in data['docs']:
            response = self.insert(doc)
            print(f"\n{response['result']}")

    def print_all(self):
        docs = self.manager.read_index_documents(self.INDEX_NAME)
        for hit in docs:
            print('------------------------')
            print('Equipment:', hit.equipment)
            print('Materials:', hit.materials)