from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import date

app = FastAPI()

Tasks = {
    1: {
        "name": "electricity_bill",
        "date": date(2026, 6, 21)
    }
}

class Task(BaseModel):
    name: str
    date: date


@app.get("/Tasks/{task_id}")
def get_task(task_id: int):
    if task_id in Tasks:
        return Tasks[task_id]

    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/Tasks/{task_id}", status_code=status.HTTP_201_CREATED)
def create_task(task_id: int, task: Task):

    if task_id in Tasks:
        raise HTTPException(status_code=409, detail="Task already exists")

    Tasks[task_id] = task.model_dump()  
    return Tasks[task_id]

@app.delete("/Tasks/{task_id}")
def delete_task(task_id:int):
    if task_id not in Tasks:
        raise HTTPException(status_code=404,detail = "Task not found")
    else:
        deleted_task = Tasks.pop(task_id)

        return {"message":"task is deleted","deleted": deleted_task}