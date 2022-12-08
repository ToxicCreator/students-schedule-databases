# app/main.py

from fastapi import FastAPI
import os
import uvicorn
app = FastAPI()


@app.get('/')
async def index():
    return {"message": "Mongo"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9001)