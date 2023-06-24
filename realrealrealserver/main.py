from fastapi import FastAPI
import openai
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
import os 
from dotenv import load_dotenv

from hashing import Hash

from fastapi import FastAPI, HTTPException, Depends, Request,status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
 credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
 return verify_token(token,credentials_exception)

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]




app = FastAPI()
load_dotenv()





mongodb_uri = os.getenv("MONGO_URI")

port = 8000

client = MongoClient(mongodb_uri,  port)
db = client["User"]


class User(BaseModel):
    username: str
    password: str
    #community: str


class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
#from main import TokenData

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str,credentials_exception):
 try:
     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
     username: str = payload.get("sub")
     if username is None:
         raise credentials_exception
     token_data = TokenData(username=username)
 except JWTError:
     raise credentials_exception

@app.post('/register')
def create_user(request:User):
   hashed_pass = Hash.bcrypt(request.password)
   user_object = dict(request)
   user_object["password"] = hashed_pass
   user_id = db["users"].insert(user_object)
   return {"res":"created"}

@app.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends()):
    user = db["users"].find_one({"username":request.username})
    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not Hash.verify(user["password"],request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    access_token = create_access_token(data={"sub": user["username"] })
    return {"access_token": access_token, "token_type": "bearer"}

@app.get('/')
def index():
    return {'data':'Hello World'}