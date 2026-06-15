from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel

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

@app.get("/contact/{contact_id}")
def get_contact(contact_id:int):
    if contact_id not in contacts:
        raise HTTPException(status_code = 404, detail = "contact not found")
    
    return contacts[contact_id]
