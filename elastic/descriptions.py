import os
from re import search
import sys
import json
from table import Table
from elasticsearch_dsl import Document
from elastic.elastic_manager import ElasticManager

<<<<<<< Updated upstream
=======
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

>>>>>>> Stashed changes

class Descriptions(Table):
    TABLE_NAME = 'description'
    INDEX_NAME = 'lessons'

<<<<<<< Updated upstream
    def __init__(self, clear=False):
=======
    def __init__(self, clear = False):
>>>>>>> Stashed changes
        self.manager = ElasticManager()
        if clear:
            self.manager.delete_index(self.INDEX_NAME)
        self.lessons_index = self.manager.create_index(
            self.INDEX_NAME
        )

<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
    def insert(self, type, description, tag, lesson_id):
        return self.manager.create_document(
            self.INDEX_NAME,
            {
<<<<<<< Updated upstream
                'type': type, 
                'description': description, 
                'tag': tag, 
=======
                'type': type,
                'description': description,
                'tag': tag,
>>>>>>> Stashed changes
                'lessonId': lesson_id
            }
        )

<<<<<<< Updated upstream

    def read(self, search):
        return self.manager.read_query(
            self.INDEX_NAME, 
            search
        )


    def update(self, query_map, new_value):
        documents = self.manager.read_query(
            self.INDEX_NAME, 
=======
    def read(self, search):
        return self.manager.read_query(
            self.INDEX_NAME,
            search
        )

    def update(self, query_map, new_value):
        documents = self.manager.read_query(
            self.INDEX_NAME,
>>>>>>> Stashed changes
            query_map
        )
        for hit in documents:
            id = hit.meta.id
            doc_type = hit.meta.doc_type
            result = self.manager.update(
<<<<<<< Updated upstream
                index=self.INDEX_NAME, 
                id=id, 
                doc_type=doc_type,
                doc=new_value
            )



    def fill(self):
        with open('./elastic/data.json', encoding='utf-8') as file:
=======
                index = self.INDEX_NAME,
                id = id,
                doc_type = doc_type,
                doc = new_value
            )

    def fill(self):
        with open('./elastic/data.json', encoding = 'utf-8') as file:
>>>>>>> Stashed changes
            data = json.load(file)
        for doc in data['docs']:
            response = self.insert(doc)
            print(f"\n{response['result']}")

<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
    def print_all(self):
        docs = self.manager.read_index_documents(self.INDEX_NAME)
        for hit in docs:
            print('------------------------')
            print('Name:', hit.Name)
            print('Type:', hit.Type)
            print('Content:', hit.Content)

<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
    def print(self, search):
        for hit in self.read(search):
            print('------------------------')
            print('Name:', hit.Name)
            print('Type:', hit.Type)
            print('Content:', hit.Content)

<<<<<<< Updated upstream

    def clear(self):
        return super().clear()


    def delete(self, query_map):
        self.manager.delete(self.INDEX_NAME, query_map)
=======
    def clear(self):
        return super().clear()

    def delete(self, query_map):
        self.manager.delete(self.INDEX_NAME, query_map)
>>>>>>> Stashed changes
