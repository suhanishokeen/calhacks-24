from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from schema import User
from passlib.context import CryptContext
from tokens import create_access_token

load_dotenv()

app = FastAPI()


client = AsyncIOMotorClient(os.getenv('MONGO_URI'))
db = client.emotion_diary

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Emotion Diary Backend!"}


@app.post("/auth/register/")
async def register(user: User):
    # Check if user exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    # Hash the password
    hashed_password = pwd_context.hash(user.password)
    
    # Insert user into the database
    user_doc = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    }
    result = await db.users.insert_one(user_doc)
    return {"message": "User registered successfully", "user_id": str(result.inserted_id)}


@app.post("/auth/login/")
async def login(user: User):
    # Find user by email
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Generate JWT token
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/auth/logout/")
def logout():
    #TODO: Implement authentication logout
    return {"message": "Logout"}


DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
HUME_API_KEY = os.getenv("HUME_API_KEY")

@app.post("/voice/upload/")
def upload_voice():
    pass

@app.post("/voice/analyze/")
def analyze_voice():
    pass

@app.post("/text/feedback/")
def feedback_text():
    pass
