from fastapi import FastAPI, HTTPException, status, Path
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

records = {
    1:{
        "name":"Dr. vinod",
        "specialization":"cardiologist",
        "consultation_fees":500
    }
}

class Doctor(BaseModel):
    name:str
    specialization:str
    consultation_fees:int

@app.post("/records/{Doctor_id}",status_code = status.HTTP_201_CREATED)
def create_Doctor(Doctor_id:int, doctor:Doctor):
    if Doctor_id in records:
        raise HTTPException(status_code=404, detail='This doctor is already registered')
    records[Doctor_id] = doctor.model_dump()
    return records[Doctor_id]

@app.get("/records/search/")
def search_by_specialization(specialization: str):
    matched_doctors = []
    
    for doctor in records.values():
        if doctor["specialization"].lower() == specialization.lower():
            matched_doctors.append(doctor)

    if not matched_doctors:
        raise HTTPException(status_code=404,detail="No doctors found with this specialization")

    return matched_doctors