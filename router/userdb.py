from fastapi import APIRouter, HTTPException, status
from db.models.user import Usuarios
from db.schema.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

routers = APIRouter(prefix="/userdb",
                    tags=["userdb"],
                    responses={404: {"message": "No Encontrado"}})





usuarios_list = []




@routers.get("/", response_model=list[Usuarios])
async def users():
    return users_schema(db_client.local.users.find())

@routers.get("/{ids}")
async def user(ids:str):
    return search_db("_id", ObjectId(ids))

@routers.get("/", response_model= Usuarios)
async def user(ids:str):
    return search_db("_id", ObjectId(ids))

@routers.post("/", response_model=Usuarios,status_code=201)
async def user(user:Usuarios):

    if type(search_db("email", user.email)) == Usuarios:
        raise HTTPException(
            status_code=404, detail="El usuario ya existe"
        )

    user_dic = dict(user)
    del user_dic["id"]

    ids = db_client.local.users.insert_one(user_dic).inserted_id

    new_user = user_schema(db_client.local.users.find_one({"_id":ids}))

    return Usuarios(**new_user)

@routers.put("/", response_model=Usuarios,status_code=200)
async def user(user:Usuarios):
    if type(search_id(user.id)) == Usuarios:
        posicion = usuarios_list.index(search_id(user.id))
        usuarios_list[posicion] = user
        return user
    else:
        raise HTTPException(status_code=404, detail="El usuario no existe")

@routers.delete("/{ids}",status_code=204)
async def user(ids:str):
    delete = db_client.local.users.find_one_and_delete({"_id":ObjectId(ids)})
    if not delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error":"no se a podido eliminar el usuario"})

def search_db(llave:str, password):
    try:
        return Usuarios(**user_schema(db_client.local.users.find_one({llave:password})))
    except:
        return {"error":"No se a encontrado el Usuario"}
