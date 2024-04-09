from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from router import productos, basic_auth_user, jwt_auth_user
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(productos.routers)
app.include_router(basic_auth_user.router)
app.include_router(jwt_auth_user.router)


app.mount("/static", StaticFiles(directory="static"), name="static")

class usuarios(BaseModel):
    id : int
    name : str
    surname : str
    url : str
    age : int

usuarios_list = [usuarios(id = 1, name = "Milton", surname = "Sandoval", url = "https://Milton.dev.com", age = 19),
                 usuarios(id = 2, name = "Pardo", surname = "Osuno", url = "https://pardososuno.com", age = 20),
                 usuarios(id = 3, name = "Rodolfo", surname = "Maloso", url = "https://rodolfomaloso.com.bo", age = 35)]




@app.get("/users", response_model=list[usuarios])
async def userlist():
    return usuarios_list

@app.get("/users/{ids}", response_model= usuarios)
async def user(ids:int):
    return search_id(ids)

@app.get("/users/", response_model= usuarios)
async def user(ids:int):
    return search_id(ids)

@app.post("/users/", response_model=usuarios,status_code=201)
async def user(user:usuarios):
    if type(search_id(user.id)) == usuarios:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    else:
        usuarios_list.append(user)
        return user

@app.put("/users/", response_model=usuarios,status_code=200)
async def user(user:usuarios):
    if type(search_id(user.id)) == usuarios:
        posicion = usuarios_list.index(search_id(user.id))
        usuarios_list[posicion] = user
        return user
    else:
        raise HTTPException(status_code=404, detail="El usuario no existe")

@app.delete("/users/{ids}", response_model= list[usuarios],status_code=200)
async def user(ids:int):
    if type(search_id(ids)) == usuarios:
        posicion = usuarios_list.index(search_id(ids))
        usuarios_list.pop(posicion)
        return usuarios_list
    else:
        raise HTTPException(status_code=404, detail="El usuario no existe")

def search_id(ids:int):
    for usuarios in usuarios_list:
        if ids == usuarios.id:
            return usuarios
    else:
        return {"error" : "No se a encontrado el usuario"}
