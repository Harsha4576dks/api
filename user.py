from fastapi import FastAPI, HTTPException, status, Path
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

users = {
    1:{
      "name":"tarun",
      "gender":"male"
    }
 }

class user(BaseModel):
     name:str
     gender:str

class updateuser(BaseModel):
     name:Optional[str]=None
     gender:Optional[str]=None
     
@app.get("/users/{user_id}")
def get_user(user_id:int = Path(..., description="The Id you want to get")):
     if user_id not in users:
          raise HTTPException(status_code = 404, detail = "user not found")
     return users[user_id]

@app.post("/users/{user_id}",status_code = status.HTTP_201_CREATED)
def post_user(user_id:int,user:user):
     if user_id in users:
          raise HTTPException(status_code = 404, detail = "user already exists")
     users[user_id] = user.model_dump()
     return users[user_id]

@app.put("/users/{user_id}")
def update_user(user_id:int, user:updateuser):
     if user_id not in users:
          raise HTTPException(status_code = 404, detail="user not found")
     current_user = users[user_id] 

     if user.name is not None:
          current_user["name"] = user.name
     if user.gender is not None:
          current_user["gender"] = user.gender
     return current_user

@app.delete("/users/{user_id}")
def delete_user(user_id:int):
     if user_id not in users:
          raise HTTPException(status_code = 404, detail="user not found")
     else:
          deleted_user = users.pop(user_id)

     return {"message":"user deleted successfully", "deleted_user":deleted_user}
