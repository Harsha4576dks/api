from fastapi import FastAPI, HTTPException, status, Path          #FastAPI -> it helps to create an app, HTTPException -> it helps to raise an exception, status -> it helps to return the status code, Path -> it helps to get the path parameter
from pydantic import BaseModel                                    #it helps to create a model for the user input, it also helps to validate the input data
from typing import Optional                                       #it helps to make the input data optional, it also helps to specify the type of the input data

app = FastAPI()

users = {

    1:{
        "name":"josh",
        "website":"www.zerotolnoeing.com",
        "age":28,
        "role":"admin"
    }
}

class User(BaseModel):
    name:str
    website:str
    age:int
    role:str

class UpdateUser(BaseModel):
    name:Optional[str] = None
    website:Optional[str] = None
    age:Optional[int] = None
    role:Optional[str] = None



@app.get("/users/{user_id}")
def get_user(user_id:int = Path(..., description="The ID you want to get")):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]


@app.post("/users/{user_id}", status_code=status.HTTP_201_CREATED)
def create_user(user_id:int, user:User):
    if user_id in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[user_id] = user.dict()
    return users[user_id]

@app.put("/users/{user_id}")
def update_user(user_id:int, user:UpdateUser):
    if user_id not in users:
        raise HTTPException(status_code=400, detail="User not found")
    current_user = users[user_id]

    if user.name is not None:
        current_user["name"] = user.name
    if user.age is not None:
        current_user["age"] = user.age
    if user.website is not None:
        current_user["website"] = user.website
    if user.role  is not None:
        current_user["role"] = user.role

    return current_user
        

@app.delete("/users/{user_id}")
def delete_user(user_id:int):
    if user_id not in users:
          raise HTTPException(status_code=400, detail="User not found")
    else:
        deleted_user = users.pop(user_id)

    return {"message": "user is deleted","deleted_user":deleted_user}

