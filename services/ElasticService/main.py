from fastapi import FastAPI
import uvicorn
import elasticsearch
import elasticsearch_dsl
import os
import time

app = FastAPI()
time.sleep(15)
client = elasticsearch.Elasticsearch('http://root:root@{0}:{1}'.format(os.getenv('ELASTIC_DBASE_IP'),
                                                                      os.getenv('ELASTIC_DBASE_PORT')))


@app.get('/')
async def index():
    return {"message": "Elastic"}

@app.get('/select')
async def select():
    return str(client.indices.create(index="maxtrushin"))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9004)