from fastapi import FastAPI, HTTPException, status, Path
from pydantic import BaseModel
from datetime import date

app = FastAPI()

Tasks = {
1:{
    "name": "electricity_bill",
    "date": date(2026,6,21)
}
}

class task(BaseModel):

    name : str
    date : str


@app.get("/Tasks:int/{task_id}")
def tasks(task_id:int):
    if task_id in Tasks:
        return Tasks[task_id]
    
    raise HTTPException(status_code = 404,detail = "task not found")