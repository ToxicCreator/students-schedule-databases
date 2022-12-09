
import os
from fastapi import FastAPI
import uvicorn
from first_request import makeFirstRequest


app = FastAPI()


@app.get('/')
async def index():
    return {
        "/make-first-request": {
            "start_date": "Начало периода обучения",
            "end_date": "Конец периода обучения",
            "term": "Заданный термин или фраза"
        },
        "/make-second-request": {},
        "/make-third-request": {}
    }


@app.get('/make-first-request')
def makeFirstRequest(start: str, end: str, term: str):
    return makeFirstRequest(start, end, term)


@app.get('/make-second-request')
def makeSecondRequest():
    pass


@app.get('/make-third-request')
def makeThirdRequest():
    pass


if __name__ == "__main__":
    port = int(os.getenv('MAIN_HUB_PORT', 9000))
    uvicorn.run(app, host="0.0.0.0", port=port)
