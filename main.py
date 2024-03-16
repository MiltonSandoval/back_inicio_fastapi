from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class usuarios(BaseModel):
    id : int
    name : str
    surname : str
    url : str
    age : int

usuarios_list = [usuarios(id = 1, name = "Milton", surname = "Sandoval", url = "https://Milton.dev.com", age = 19),
                 usuarios(id = 2, name = "Pardo", surname = "Osuno", url = "https://pardososuno.com", age = 20),
                 usuarios(id = 3, name = "Rodolfo", surname = "Maloso", url = "https://rodolfomaloso.com.bo", age = 35)]


@app.get("/users")
async def users():
    return "Hola users"

@app.get("/users/list")
async def userlist():
    return usuarios_list

@app.get("/users/{ids}")
async def user(ids:int):
    return search_id(ids)

@app.get("/users/")
async def user(ids:int):
    return search_id(ids)


def search_id(ids:int):
    for usuarios in usuarios_list:
        if ids == usuarios.id:
            return usuarios
    else:
        return {"error" : "No se a encontrado el usuario"}
