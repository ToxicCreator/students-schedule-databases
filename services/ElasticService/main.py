from elastic_manager import ElasticManager
from fastapi import FastAPI
import uvicorn

app = FastAPI()
manager = ElasticManager()


@app.get('/')
async def index():
    return {"message": "Elastic"}


@app.get('/description')
async def description(term: str):
    return manager.read_query('lessons', {
        'materials': term
    })


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9004)