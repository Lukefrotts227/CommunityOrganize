from fastapi import FastAPI

from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
import os 
from dotenv import load_dotenv

from hashing import Hash

from fastapi import FastAPI, HTTPException, Depends, Request,status
from oauth import get_current_user
from jwttoken import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]




app = FastAPI()
load_dotenv()





mongodb_uri = os.getenv("MONGO_URI")

port = 8000

client = MongoClient(mongodb_uri,  port)
db = client["User"]


class User(BaseModel):
    username: str
    company: str
    password: str


class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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