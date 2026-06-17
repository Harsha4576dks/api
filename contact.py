from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

contacts = {
   1:{
       "name":"kumar",
       "number":9885532166
   } 
}

class user(BaseModel):
    name:str
    number:int

class updateuser(BaseModel):
    name:Optional[str]=None
    number:Optional[str]=None

@app.get("/contact/{contact_id}")
def get_contact(contact_id:int):
    if contact_id not in contacts:
        raise HTTPException(status_code = 404, detail = "contact not found")
    
    return contacts[contact_id]

@app.post("/contact/{contact_id}", status_code=status.HTTP_201_CREATED)
def create_user(contact_id:int, contact:user):
    if contact_id in contacts:
        raise HTTPException(status_code=404, detail="contact already exist")

    contacts[contact_id] = contact.model_dump()
    return contacts[contact_id]

@app.put("/contact/{contact_id}")
def update_user(contact_id:int, contact:updateuser):
    if contact_id not in contacts:
        raise HTTPException(status_code=404, detail = "contact does not  exist")
    current_contact = contacts[contact_id]

    if contact.name is not None:
        current_contact["name"] = contact.name
    if contact.number is not None:
        current_contact["number"] = contact.number

    return current_contact

@app.delete("/contact/{contact_id}")
def delete_user(contact_id:int):
    if contact_id not in contacts:
        raise HTTPException(status_code=404,detail = "contact not found")
    else:
        deleted_user = contacts.pop(contact_id)

    return {"message":"contact  deleted  sucessfully","deleted_user":deleted_user}

