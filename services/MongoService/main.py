# app/main.py
import uvicorn
from fastapi import FastAPI
from mongo_manager import MongoManager
import pymongo
import os
import time

app = FastAPI()
manager = MongoManager("microservices")
time.sleep(10)
mongo = pymongo.MongoClient(host=os.getenv('MONGO_DBASE_IP'),
                    port=int(os.getenv('MONGO_DBASE_PORT_SECOND')))
db = mongo[str(os.getenv('MONGO_DBASE_NAME'))]
collection = db[str(os.getenv('MONGO_COLLECTION_NAME'))]


@app.get('/')
async def index():
    return {"message": "Mongo"}

@app.get('/select')
async def select():
    return str(collection.insert_one({
        "name": "КБ-1",
        "specialities": [
            {
                "code": "10.03.01",
                "name": "Информационная безопасность"
            },
            {
                "code": "10.05.03",
                "name": "Информационная безопасность автоматизированных систем"
            }
        ]
    }))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9001)