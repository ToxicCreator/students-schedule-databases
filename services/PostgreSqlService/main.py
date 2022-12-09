import uvicorn
from fastapi import FastAPI
from psql_manager import PsqlManager


app = FastAPI()
manager = PsqlManager()

@app.get('/')
async def index():
    return {"message": "PostgreSQL"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9005)