from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/')
async def index():
    return {"message": "Neo4j"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9002)