from fastapi import FastAPI, HTTPException, status, Path
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

records = {
    1:{
        "name":"Dr.vinod",
        "specialization":"cardiologist",
        "experience":5,
        "consultation_fees":500
    }
}

class Doctor(BaseModel):
    name:str
    specialization:str
    experience:int
    consultation_fees:int

class updateDoctor(BaseModel):
    name:str|None=None
    specialization:str|None=None
    experience:int|None=None
    consultation_fees:int|None=None

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

@app.put("/records/{Doctor_id}")
def update_Doctor(Doctor_id:int, Doctor:updateDoctor):
   if Doctor_id not in records:
        raise HTTPException(status_code = 400, detail = "This doctor is not available in the list") 

   for key, value in Doctor.model_dump(exclude_unset = True).items():
    if value is not None:
        records[Doctor_id][key] = value
            
    return {"message":"This doctors data is updated successsfully", "updated_Doctor":records[Doctor_id]}
   
   