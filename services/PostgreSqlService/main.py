from fastapi import FastAPI
import uvicorn
import psycopg2

app = FastAPI()


@app.get('/')
async def index():
    return {"message": "PostgreSQL"}

@app.get('group-lessons-by-id')
def group_lessons_by_id(group_id):
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9005)