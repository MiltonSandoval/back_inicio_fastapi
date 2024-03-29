from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class usuarios(BaseModel):
    username : str
    full_name : str
    email : str
    disable : bool

class userdb(usuarios):
    password : str

users_db = {
    "Pardo":{
        "username" : "Pardo",
        "full_name" : "Milton Sandoval",
        "email" : "sandoval@yopmail.com",
        "disable" : False,
        "password" : "123456"
    },
    "Pardo2":{
        "username" : "Pardo2",
        "full_name" : "Milton pardoso",
        "email" : "sandoval2@yopmail.com",
        "disable" : True,
        "password" : "654321"
    }
}

def search_userdb(username: str):
    if username in users_db:
        return userdb(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return usuarios(**users_db[username])

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticacion invalidos",
            headers={"WWW-Authenticate":"Bearer"})
    if user.disable:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Usuario Inactivo")
    return user

@app.post("/login")
async def login(form : OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    user = search_userdb(form.username)
    if not user.password == form.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contrasena no es correcto")
    return {"access_token": user.username, "token_type":"Bearer"}

@app.get("/user/me")
async def me(user: usuarios = Depends(current_user)):
    return user
