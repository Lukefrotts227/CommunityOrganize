from fastapi import FastAPI
import openai
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
import os 
from dotenv import load_dotenv
from passlib.context import CryptContext

from hashing import Hash

from fastapi import FastAPI, HTTPException, Depends, Request,status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]




app = FastAPI(debug=True)


load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


mongodb_uri = os.getenv("MONGO_URI")

port = 8000

client = MongoClient(mongodb_uri,  port)
db = client["User"]
users_collection = db["users"]

class User(BaseModel):
    username: str
    password: str
    community: str


class Login(BaseModel):
    username: str
    password: str

class Communiy(BaseModel):
    country: str 
    state: str
    town: str


def community_handle():
    pass


'''
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
'''

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
print('hello there')
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

'''
# Function to verify the password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Function to create the access token
def create_access_token(username):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
'''



'''
# Function to authenticate a user
def authenticate_user(username, password):
    user = db.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        return False
    return True
'''
'''
@app.post("/login")
def login(login_data: Login): 
    username = login_data.username
    password = login_data.password
    user = collecton.find_one({"username": username})
    if user and user['password'] == password: 
        return {"message": "Login Success"}
    raise HTTPException(status_code=401, detail="Invalid username or password")
'''
'''
# Route to handle user login
@app.post("/login")
def login(username: str, password: str):
    if not authenticate_user(username, password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(username)
    return {"access_token": access_token, "token_type": "bearer"}
'''
'''
@app.post('/register')
def create_user(request:User):
   hashed_pass = Hash.bcrypt(request.password)
   user_object = dict(request)
   user_object["password"] = hashed_pass
   user_id = db["users"].insert(user_object)
   return {"res":"created"}
'''

@app.post("/register")
def register(user: User):
    # Check if the username is already taken
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Create a new user document
    new_user = {
        "username": user.username,
        "password": user.password
    }

    # Insert the new user into the collection
    users_collection.insert_one(new_user)

    return {"message": "Registration successful"}


@app.post("/login")
def login(login: Login):
    # Find the user by username
    user = users_collection.find_one({"username": login.username})
    if user and user['password'] == login.password:
        return {"message": "Login successful"}

    raise HTTPException(status_code=401, detail="Invalid username or password")

'''
@app.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends()):
    user = db["users"].find_one({"username":request.username})
    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not Hash.verify(user["password"],request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    access_token = create_access_token(data={"sub": user["username"] })
    return {"access_token": access_token, "token_type": "bearer"}
'''
@app.get('/')
def index():
    return {'data':'Hello World'}