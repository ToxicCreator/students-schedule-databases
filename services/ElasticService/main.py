from fastapi import FastAPI
import uvicorn
app = FastAPI()


@app.get('/')
async def index():
    return {"message": "Elastic"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9004)