from fastapi import FastAPI, HTTPException, status, Path
from pydantic import BaseModel
from typing import Optional

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

class updatestudent(BaseModel):
    name:Optional[str]=None
    grade:Optional[str]=None
    section:Optional[str]=None
    status:Optional[str]=None


@app.get("/students/{student_id}")
def get_student(student_id:int = Path(..., description="The ID ou want to get")):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="student not found")
    return students[student_id]

@app.post("/students/{student_id}", status_code=status.HTTP_201_CREATED)
def post_student(student_id:int, student:student):
    if student_id in students:
        raise HTTPException(status_code=404, detail="student is already present")
    students[student_id] = student.model_dump()
    return students[student_id]

@app.put("/students/{student_id}")
def update_student(student_id:int, student:updatestudent):
    if student_id not in students:
        raise HTTPException(status_code=400, detail = "student not found")
    current_student=students[student_id]

    if student.name is not None:
        current_student["name"] = student.name
    if student.grade is not None:
        current_student["grade"] = student.grade
    if student.section is not None:
        current_student["section"] = student.section
    if student.status is not None:
        current_student["status"] = student.status

    return current_student

@app.delete("/students/{student_id}")
def delete_student(student_id:int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="student not found")
    else:
        deleted_student = students.pop(student_id)

    return{"message":"deleted sucessfully", "deleted_student" : deleted_student}

@app.get("/students/search/")
def search_by_name(name:Optional[str]=None):
    if not name:
        return {"message":"name is required"}
    for student in students.values():
        if student["name"] == name:
            return student
        
    raise HTTPException(status_code=404, detail="student notfound")