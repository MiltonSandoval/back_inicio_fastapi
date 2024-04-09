from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "62849474edb096f9644b3ee233bbbf67a24bb136d13e5b6722f6f749ec2f56ce"

router = APIRouter()


oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

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
        "password" : "$2a$12$JuJlBxb3qOtp9ae6sH2sMOHyiYxW7zQ3SK3.cWZGxCUl7trQJIg8u"
    },
    "Pardo2":{
        "username" : "Pardo2",
        "full_name" : "Milton pardoso",
        "email" : "sandoval2@yopmail.com",
        "disable" : True,
        "password" : "$2a$12$OAKIUHofYgKrGh/BnQS8EOjlh46cCf2gWMzCmbZpQLkqYGvo3keRe"
    }
}

def search_userdb(username: str):
    if username in users_db:
        return userdb(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return usuarios(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):

    exeception = HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticacion invalidos",
            headers={"WWW-Authenticate":"Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exeception

    except JWTError:
        raise exeception

    return search_user(username)


async def current_user(user: usuarios = Depends(auth_user)):
    if user.disable:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Usuario Inactivo")
    return user


@router.post("/login")
async def login(form : OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_userdb(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contrasena no es correcto")

    access_token = {"sub": user.username,
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token,SECRET, algorithm=ALGORITHM), "token_type":"Bearer"}

@router.get("/user/me")
async def me(user: usuarios = Depends(current_user)):
    return user
