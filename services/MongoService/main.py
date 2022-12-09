import uvicorn
from fastapi import FastAPI
from mongo_manager import MongoManager

app = FastAPI()
manager = MongoManager("microservices")


@app.get('/')
async def index():
    return {"message": "Mongo"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9001)