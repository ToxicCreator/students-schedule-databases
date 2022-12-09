from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/')
async def index():
    return {"message": "Neo4j"}

@app.post('/count_of_students')
async def student_count_by_group(groups_id: list):
    student_count = []
    for group_id in groups_id:
        query = f'MATCH (:Course {{name:\'{group_id}\'}})->[r:member_of]->(:Group) RETURN count(r);'
        student_count.append(self.execute(query).values())
    return sum(student_count)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9002)