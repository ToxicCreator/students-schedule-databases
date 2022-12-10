from fastapi import FastAPI
import uvicorn
import neo4j
import os
import time

app = FastAPI()
time.sleep(10)
database = neo4j.GraphDatabase.driver(
    uri="bolt://{0}:{1}".format(os.getenv('NEO4J_DBASE_IP'), int(os.getenv('NEO4J_DBASE_PORT_SECOND'))),
    auth=(str(os.getenv('NEO4J_DBASE_LOGIN')), str(os.getenv('NEO4J_DBASE_PASSWORD'))),
    max_connection_pool_size=100000)
session = database.session()


@app.get('/')
async def index():
    return {"message": "Neo4j"}

@app.get('/select')
async def select():
    query = 'MATCH (n) RETURN n;'
    return session.run(query).values()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9002)