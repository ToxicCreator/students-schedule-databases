from fill.fill_manager import fill
from fastapi import FastAPI
import os
import uvicorn
import time

time.sleep(5)
app = FastAPI()

@app.get('/')
async def index():
    return {"message": "PostgreSQL"}

@app.get('/fill')
async def try_to_fill():
    if fill():
        return "Fill successful"
    else:
        return "Fill failed"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9006)