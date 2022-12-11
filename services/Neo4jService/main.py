from fastapi import FastAPI
import uvicorn
import os
import time
from neo4j_manager import Neo4jManager


app = FastAPI()
time.sleep(10)
manager = Neo4jManager()


@app.get('/')
async def index():
    return {"message": "Neo4j"}


@app.get('/select')
async def select():
    query = 'MATCH (n) RETURN n;'
    return session.run(query).values()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9002)
