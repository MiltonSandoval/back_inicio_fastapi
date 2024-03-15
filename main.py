from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class usuarios(BaseModel):
    name : str
    surname : str
    url : str
    age : int

usuarios_list = [usuarios(name = "Milton", surname = "Sandoval", url = "https://Milton.dev.com", age = 19),
                 usuarios(name = "Pardo", surname = "Osuno", url = "https://pardososuno.com", age = 20),
                 usuarios(name = "Rodolfo", surname = "Maloso", url = "https://rodolfomaloso.com.bo", age = 35)]


@app.get("/users")
async def users():
    return "Hola users"

@app.get("/users/list")
async def userlist():
    return usuarios_list

