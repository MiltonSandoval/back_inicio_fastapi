from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class usuarios(BaseModel):
    username : str
    full_name : str
    email : str
    disable : bool

class userdb(usuarios):
    password : str

user_db = {
    "Milton":{
        "username" : "Pardo",
        "full_name" : "Milton Sandoval",
        "email" : "sandoval@yopmail.com",
        "disable" : False,
        "password" : "123456"
    },
    "Milton2":{
        "username" : "Pardo2",
        "full_name" : "Milton pardoso",
        "email" : "sandoval2@yopmail.com",
        "disable" : True,
        "password" : "654321"
    }
}

def search_user(username: str):
    if username in user_db:
        return userdb(user_db[username])
