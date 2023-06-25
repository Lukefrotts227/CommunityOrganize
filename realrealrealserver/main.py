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
openai_key = os.getenv("OPENAI_KEY")

openai.api_key = openai_key


port = 8000

client = MongoClient(mongodb_uri,  port)
db = client["User"]
users_collection = db["users"]
community_collection = db["community"]
post_collection = db["posts"]


class Register(BaseModel):
    username: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class Community(BaseModel):
    user: str 
    state: str
    town: str

class Post(BaseModel): 
    title: str
    contents: str
    creator: str
    






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


def generate_community_phrase():
    # Community-related prompt
    prompt = "Community is like a"

    # Make the API call to OpenAI
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=20,  # Adjust the number of tokens as per your requirements
        temperature=0.5,  # Adjust the temperature value to control the output randomness
        top_p=1.0,  # Adjust the top_p value to control the diversity of the output
        n=1,  # Adjust the number of responses to generate
        stop=None,  # You can specify a custom stop sequence if needed
        timeout=15,  # Timeout in seconds (optional)
    )

    # Retrieve the generated phrase from the API response
    if 'choices' in response and len(response['choices']) > 0:
        phrase = response['choices'][0]['text'].strip()
        return phrase
    else:
        return None

def summarize_text(text):
    # Make the API call to OpenAI
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=text,
        max_tokens=100,  # Adjust the number of tokens as per your requirements
        temperature=0.3,  # Adjust the temperature value to control the output randomness
        top_p=1.0,  # Adjust the top_p value to control the diversity of the output
        n=1,  # Adjust the number of responses to generate
        stop=None,  # You can specify a custom stop sequence if needed
        timeout=15,  # Timeout in seconds (optional)
    )

    # Retrieve the summarized text from the API response
    if 'choices' in response and len(response['choices']) > 0:
        summary = response['choices'][0]['text'].strip()
        return summary
    else:
        return None

# giving community data
@app.get("/givecom")
def giveCom():
    pass

# give post data 
@app.get("/giveposts")
def givePosts(): 
    pass

@app.post("/createpost")
def getpost(post: Post):
    username = post.creator
    contents = post.contents
    title = post.title
    user = users_collection.find_one({"username": username})
    state = user["state"]
    town = user["town"]
    title = state + " " + town + ": " + title
    findTitle = post_collection.find_one({"title": title})

    if not findTitle == None : 
        raise HTTPException(status_code=400, detail="Title is not unique")
    
    summary = summarize_text(contents)

    new_post = {
        "content" : contents,
        "user": user,
        "title": title,
        "summary": summary

    }


    result = post_collection.insert_one(new_post)

    return {"message": "post has been sent"}


@app.post("/register")
def register(user: Register):
    print(user)
    # Check if the username is already taken
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Create a new user document
    new_user = {
        "username": user.username,
        "password": user.password,
        "has_community": False
    }

    # Insert the new user into the collection
    users_collection.insert_one(new_user)

    return {"message": "Registration successful"}

@app.post("/community")
def community(community: Community): 
    town = community.town
    state = community.state 
    user = community.user

    query1 = {"state": state}
    query2 = {"town": town}
    query3 = {"username": user}

    res = community_collection.find_one(query1)
    if res is None: 
        result = community_collection.insert_one({
            "state": state, 
            "town": town
        })
        update_query = {
            "$set": {"state": state, "town": town, "has_community": True}
        }
        res = users_collection.update_one(query3, update_query)
        return {"message": "You are the first member of a community"}
        
    else: 
        res2 = community_collection.find_one({"$and": [query1, query2]})
        if res2 is None:
            result = community_collection.insert_one({
                "state": state, 
                "town": town
            })
            update_query = {
                "$set": {"state": state, "town": town, "has_community": True}
            }
            res = users_collection.update_one(query3, update_query)
            return {"message": "You are the first member of a community"}
    
    update_query = {
        "$set": {"state": state, "town": town, "has_community": True}
    }
    result = users_collection.update_one(query3, update_query)

    return {"message": "Success found a community for you"}




    
    


        

@app.post("/login")
def login(login: Login):
    print(login)
    # Find the user by username
    user = users_collection.find_one({"username": login.username})
    if user and user['password'] == login.password:
        return {"message": "Login successful"}

    raise HTTPException(status_code=401, detail="Invalid username or password")


@app.get('/')
def index():
    return {'data':generate_community_phrase()}