from fastapi import FastAPI
import uvicorn
import redis
import os

redis_db = redis.Redis(
            host=str(os.getenv('REDIS_DBASE_IP')),
            port=os.getenv('REDIS_DBASE_PORT'),
            db=int(os.getenv('REDIS_DB')),
            charset=str(os.getenv('REDIS_CHARSET')),
            decode_responses=True
        )
app = FastAPI()


@app.get('/')
async def index():
    return {"message": "Redis"}

@app.get('/select')
async def select():
    redis_db.hset("123", 'name', 'name')
    student = redis_db.hgetall('123')
    return str(student)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9003)