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
async def userlist():
    return usuarios_list

@app.get("/users/{ids}")
async def user(ids:int):
    return search_id(ids)

@app.get("/users/")
async def user(ids:int):
    return search_id(ids)

@app.post("/users/")
async def user(user:usuarios):
    if type(search_id(user.id)) == usuarios:
        return {"error":"El usuario ya existe"}
    else:
        usuarios_list.append(user)
        return user

@app.put("/users/")
async def user(user:usuarios):
    if type(search_id(user.id)) == usuarios:
        posicion = usuarios_list.index(search_id(user.id))
        usuarios_list[posicion] = user
        return user
    else:
        return {"usuario no existe"}

@app.delete("/users/{ids}")
async def user(ids:int):
    if type(search_id(ids)) == usuarios:
        posicion = usuarios_list.index(search_id(ids))
        usuarios_list.pop(posicion)
        return usuarios_list
    else:
        return {"usuario no existe"}

def search_id(ids:int):
    for usuarios in usuarios_list:
        if ids == usuarios.id:
            return usuarios
    else:
        return {"error" : "No se a encontrado el usuario"}
