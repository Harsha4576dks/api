from fastapi import FastAPI,  HTTPException, status, Path
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

pets = {
  1:  {
     "name":"jaggu",
     "breed":"husky",
     "age":7
    }
}

class pet(BaseModel):
    name:str
    breed:str
    age:int

class updatepet(BaseModel):
    name:Optional[str] = None
    breed:Optional[str] = None
    age:Optional[int] = None

@app.get("/pets/{pet_id}")
def get_pet(pet_id:int = Path(..., description = "The id you want")):
    if pet_id not in pets:
        raise HTTPException(status_code = 404, detail = "This pet's detail is not available")
    return pets[pet_id]

@app.post("/pets/{pet_id}", status_code = status.HTTP_201_CREATED)
def create_pet(pet_id:int, pet:pet):
    if pet_id in pets:        
        raise HTTPException(status_code = 404, detail = "This pet's detail is already available")
    pets[pet_id] = pet.model_dump()
    return pets[pet_id]

@app.put("/pets/{pet_id}")
def update_pet(pet_id:int,  pet:updatepet):
    if pet_id not in pets:
        raise HTTPException(status_code = 404, detail = "This pet's detail does not exist")
    current_pet = pets[pet_id]

    if pet.name is not None:
        current_pet["name"] = pet.name
    if pet.breed  is not None:
        current_pet["breed"] = pet.breed
    if pet.age is not None:
        current_pet["age"] = pet.age
    else:
        print("add pet's detail")
    return current_pet

@app.delete("/pets/{pet_id}")
def delete_pet(pet_id:int):
    if pet_id not in pets:
        raise HTTPException(status_code = 404, detail = "This pet's detail is already available")    
    else:
        deleted_pet = pets.pop(pet_id)
    return {"message":"this pet has been deleted successfully", "deletd_pet":deleted_pet}

@app.get("/pets/search/")
def search_by_name(name:Optional[str] = None):
    if not name:
        return {"message":"name parameter required"}
    
    for pet in pets.values():
        if pet["name"] == name:
            return pet
    raise HTTPException(status_code = 404, detail = "This pet's detail is not found")