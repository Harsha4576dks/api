from fastapi import FastAPI, HTTPException, status, Path
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

vehicles = {
    1:{
        "owner":"kiran",
        "car":"BMW"
    }
}

class vehicle(BaseModel):
    owner:str
    car:str

class updatevehicle(BaseModel):
    owner:Optional[str]=None
    car:Optional[str]=None


@app.get("/vehicles/{vehicle_id}")
def get_vehicle(vehicle_id:int = Path(..., description="the ID you want to get")):
    if vehicle_id not in vehicles:
        raise HTTPException(status_code=404, detail = "vehicle not found")
    return vehicles[vehicle_id]    

@app.post("/vehicles/{vehicle_id}",status_code = status.HTTP_201_CREATED)
def create_vehicle(vehicle_id:int, vehicle:vehicle):
    if vehicle_id in vehicles:
        raise HTTPException(status_code=400, detail="vehicle already exists")
    vehicles[vehicle_id] = vehicle.model_dump()
    return vehicles[vehicle_id]

@app.put("/vehicles/{vehicle_id}")
def update_vehicle(vehicle_id:int, vehicle:updatevehicle):
    if vehicle_id not in vehicles:
        raise HTTPException(status_code=404, detail="vehicle not found")
    current_vehicle = vehicles[vehicle_id]

    if vehicle.owner not in vehicles:
        current_vehicle["owner"] = vehicle.owner
    if vehicle.car not in vehicles:
        current_vehicle["car"] = vehicle.car

    return current_vehicle

@app.delete("/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id:int):
    if vehicle_id not in vehicles:
        raise HTTPException(status_code=404, detail="vehicle not found")
    else:
        deleted_vehicle = vehicles.pop(vehicle_id)

    return {"message":"deleted successfully", "deleted_vehicle": deleted_vehicle}