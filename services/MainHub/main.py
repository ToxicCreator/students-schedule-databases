from fastapi import FastAPI
import uvicorn
import requests

app = FastAPI()


@app.get('/')
async def index():
    return {"message": "MainHub"}


@app.get('/makeFirstRequest')
def makeFirstRequest():
    pass


@app.get('/makeSecondRequest')
def makeSecondRequest():
    pass


@app.get('/makeThirdRequest')
def makeThirdRequest():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
