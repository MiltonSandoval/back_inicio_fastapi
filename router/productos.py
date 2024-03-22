from fastapi import APIRouter
from pydantic import BaseModel

routers = APIRouter(prefix="/productos",
                    tags=["productos"],
                    responses={404: {"message": "No Encontrado"}})

class productos(BaseModel):
    id : int
    name : str
    precio : int

products_list = [productos(id = 1, name = "Cuaderno",precio = 19),
                 productos(id = 2, name = "Lapiz",precio = 1),
                 productos(id = 3, name = "Borrador",precio = 2)]




@routers.get("/", response_model=list[productos])
async def product_list():
    return products_list

