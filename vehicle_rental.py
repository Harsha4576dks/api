from fastapi import FastAPI, HTTPException, status, Path
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

customer_details  = {
    1:{
        "name":"dhruva",
        "DL_number":"KA 05 5481534",
        "email":"dhruv@gmail.com",
        "phone":89456153
            }
}

vehicles = {
    1:{
        "vehicle_name":"activa",
        "vehicle_type":"scooter",
        "price_per_hour":5
    }
        
    }


class Customer(BaseModel):
    name:str
    DL_number:str
    email:str
    phone:int

class Vehicle(BaseModel):
   vehicle_name:str
   vehicle_type:str
   price_per_hour:int

class Updatecustomer_details(BaseModel):
    DL_number:Optional[str] = None
    email:Optional[str] = None
    phone:Optional[str] = None

class rental(BaseModel):
    customer_id:int
    vehicle_id:int
    hours:int
    

@app.get("/customer_details/{customer_id}")
def get_customer_details(customer_id:int = Path(..., description = "The ID you want")):
    if customer_id not in customer_details:
        raise HTTPException(status_code=404, detail="customer not found")
    return customer_details[customer_id]

@app.post("/customer_details/{customer_id}", status_code  = status.HTTP_201_CREATED)
def add_customer(customer_id:int, customer:Customer):
    if customer_id in customer_details:
        raise HTTPException(status_code=404, detail="customer already exists")
    customer_details[customer_id] = customer.model_dump()
    return customer_details[customer_id]

@app.patch("/customers/{customer_id}")
def update_customer_details(customer_id:int, customer:Updatecustomer_details ):
    if customer_id not in customer_details:
        raise HTTPException(status_code=404, detail="customer already exists")
    
    for key, value in customer.model_dump(exclude_unset=True).items():
        customer_details[customer_id][key] = value
    return customer_details[customer_id]

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id:int):
    if customer_details[customer_id] is None:
        raise HTTPException(status_code=404, detail="customer not found")
    else:
        deleted_customer = customer_details.pop(customer_id)

    return {"message":"customer deleted successfully", "deleted_customer" : deleted_customer}

@app.post("/vehicles/{vehicle_id}",status_code=status.HTTP_201_CREATED)
def post_vehicle(vehicle_id:int, vehicle:Vehicle):
    if vehicle_id in vehicles:
        raise HTTPException(status_code=404, detail="vehicle  not found")
    vehicles[vehicle_id] = vehicle.model_dump()
    return vehicles[vehicle_id]

@app.get("/vehicles/{vehicle_id}")
def get_vehicle(vehicle_id:int = Path(..., description="the id you want")):
    if vehicle_id not in vehicles:
        raise HTTPException(status_code=404, detail="vehicle not found")
    return vehicles[vehicle_id]

@app.post("/rent")
def calculate_rent( rent:rental):
    if rent.customer_id not in customer_details:
        raise HTTPException(status_code=404, detail="customer  not found")
    if rent.vehicle_id not in vehicles:
        raise HTTPException(status_code=404, detail="vehicle  not found")
    
    price_per_hour = vehicles[rent.vehicle_id]["price_per_hour"]
    hours = rent.hours
    total_amount = price_per_hour * hours

    return {
        "customer_id":rent.customer_id,
        "customer_name":customer_details[rent.customer_id]["name"],
        "vehicle_id":rent.vehicle_id,
        "vehicle_name":vehicles[rent.vehicle_id]["vehicle_name"],
        "hours":rent.hours,
        "price_per_hour":price_per_hour,  
        "total_amount":total_amount
        }