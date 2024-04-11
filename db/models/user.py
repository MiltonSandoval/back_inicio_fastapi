from pydantic import BaseModel



class Usuarios(BaseModel):
    id : str = None
    username : str
    email : str
