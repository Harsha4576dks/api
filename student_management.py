from fastapi import FastAPI, HTTPException, status, Path
from pydantic import BaseModel

app = FastAPI()

students = {

    1:{
         "name":"bhuvan",
         "grade":"5",
         "section":"A",
         "Status":"present"
    }
}

class student(BaseModel):
    name:str
    grade:int
    section:str
    status:str

@app.get("/students/{student_id}")
def get_student(student_id:int = Path(..., description="The ID ou want to get")):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="student not found")
    return students[student_id]

@app.post("/students{student_id}", status_code=status.HTTP_201_CREATED)
def post_student(student_id:int, student:student):
    if student_id in students:
        raise HTTPException(status_code=404, detail="student is already present")
    students[student_id] = student.model_dump()
    return students[student_id]