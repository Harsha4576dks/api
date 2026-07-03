from fastapi import FastAPI, HTTPException, status, Path
from pydantic import BaseModel
from typing import Optional

apple = FastAPI()

teachers = {
    1:{
        "name":"kavitha",
        "Class":"6std"
    }
}

class student(BaseModel):
    name:str
    Class:str

class updatestudent(BaseModel):
    name:Optional[str]=None
    Class:Optional[str]=None

@apple.get("/teacher/{student_id}")
def get_student(student_id:int=Path(...,description="The  id you want")):
    if student_id not in teachers:
        raise HTTPException(status_code=404, detail="the student is not of this class")
    return teachers[student_id]

@apple.post("/teachers/{student_id}", status_code=status.HTTP_201_CREATED)
def post_student(student_id:int, student:student):
    if student_id in teachers:
        raise HTTPException(status_code =  404, detail = "this student is already admitted")
    teachers[student_id]=student.model_dump()
    return teachers[student_id]

@apple.put("/teachers/{student_id}")
def update_student(student_id:int, student:updatestudent):
    if student_id not in teachers:
        raise HTTPException(status_code=404, detail=" this student is not in the list")
    current_student = teachers[student_id]

    if student.name is not None:
        current_student["name"] = student.name
    if student.Class is not None:
        current_student["Class"] = student.Class
    return current_student

@apple.delete("/teachers/{student_id}")
def delete_student(student_id:int):
    if student_id not in teachers:
        raise HTTPException(status_code=404,detail="The student is not present in the list")
    deleted_student = teachers.pop(student_id)

    return {"message":"deleted successully", "deleted_student" : deleted_student}