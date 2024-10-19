from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import requests
import websockets
import asyncio
import json
import bcrypt
import base64
from pathlib import Path
import tempfile
from pydub import AudioSegment
from collections import defaultdict, Counter
import statistics
from typing import List, Dict, Any



load_dotenv()

app = FastAPI()

# Database setup
client = AsyncIOMotorClient(os.getenv('MONGO_URI'))
db = client.emotion_diary

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for JWT")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7  # Long-lived refresh token

HUME_API_KEY = os.getenv("HUME_API_KEY")
HUME_WEBSOCKET_URL = f"wss://api.hume.ai/v0/stream/models?apikey={HUME_API_KEY}"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic models
class User(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print(f"Error encoding JWT: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create access token")

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print(f"Error encoding refresh token: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create refresh token")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await db.users.find_one({"email": email})
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to the Emotion Diary Backend!"}


@app.post("/auth/register/", response_model=dict)
async def register(user: User):
    existing_user = await db.users.find_one({"email": user.email})
    existing_username = await db.users.find_one({"username": user.username})

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists, email checks out")
    if existing_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists, username checks out")
    
    hashed_password = hash_password(user.password)
    user_doc = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    }
    result = await db.users.insert_one(user_doc)
    return {"message": "User registered successfully", "user_id": str(result.inserted_id)}


@app.post("/auth/login/", response_model=Token)
async def login(user: User):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    try:
        access_token = create_access_token({"sub": user.email})
        refresh_token = create_refresh_token({"sub": user.email})
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except Exception as e:
        print(f"Error creating access or refresh token: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create tokens")

@app.post("/auth/refresh/", response_model=Token)
async def refresh_token(refresh_token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Generate a new access token
    try:
        new_access_token = create_access_token({"sub": email})
        return {"access_token": new_access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except Exception as e:
        print(f"Error refreshing access token: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not refresh access token")



# Improved error handling: Using logging for errors and exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    print(f"An error occurred: {exc}")
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# Example protected route
@app.get("/protected/")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "You have access to this protected route!", "user": current_user}

class AudioChunkProcessor:
    def __init__(self, chunk_size_ms: int = 5000):
        self.chunk_size_ms = chunk_size_ms
        self.all_emotions = defaultdict(list)
        self.segments_emotions = []
        self.top_emotions_counter = Counter()

    
    def split_audio(self, audio_path: str) -> List[AudioSegment]:
        """Split audio file into 5-second chunks"""
        audio = AudioSegment.from_file(audio_path)
        chunks = []
        
        for i in range(0, len(audio), self.chunk_size_ms):
            chunk = audio[i:i + self.chunk_size_ms]
            chunks.append(chunk)
        
        return chunks

    def encode_audio_chunk(self, chunk: AudioSegment) -> str:
        """Encode audio chunk to base64"""
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            chunk.export(temp_file.name, format='mp3')
            with open(temp_file.name, 'rb') as fp:
                encoded_data = base64.b64encode(fp.read()).decode('utf-8')
            os.unlink(temp_file.name)
            return encoded_data

    async def process_chunk(self, chunk: AudioSegment, start_time: float, websocket) -> Dict:
        """Process a single audio chunk through Hume AI"""
        encoded_chunk = self.encode_audio_chunk(chunk)
        
        message = {
            "models": {
                "prosody": {}
            },
            "data": encoded_chunk
        }
        
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        result = json.loads(response)
        
        return self.process_emotions(result, start_time)

    def process_emotions(self, result: Dict, start_time: float) -> Dict:
        """Process emotions from a chunk result"""
        if 'prosody' not in result or 'predictions' not in result['prosody']:
            return None
            
        predictions = result['prosody']['predictions']
        chunk_emotions = []
        
        for pred in predictions:
            emotions = pred['emotions']
            top_emotions = sorted(emotions, key=lambda x: x['score'], reverse=True)[:3]
            
            segment_data = {
                "timestamp": start_time + pred['time']['begin'],
                "emotions": [
                    {"name": emotion['name'], "score": round(emotion['score'], 3)}
                    for emotion in top_emotions
                ]
            }
            
            chunk_emotions.append(segment_data)

            # Count top emotion for each prediction
            if top_emotions:
                self.top_emotions_counter[top_emotions[0]['name']] += 1
            
            
            # Add to overall emotions
            for emotion in emotions:
                self.all_emotions[emotion['name']].append(emotion['score'])
        
        return chunk_emotions

    def get_overall_emotions(self) -> List[Dict]:
        """Calculate overall emotions from all processed chunks"""
        overall_emotions = {}
        for emotion, scores in self.all_emotions.items():
            overall_emotions[emotion] = statistics.mean(scores)
        
        top_overall = sorted(
            overall_emotions.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        return [
            {"name": name, "score": round(score, 3)}
            for name, score in top_overall
        ]

    def get_most_common_top_emotions(self) -> List[Dict]:
        """Get the most common top emotions across all chunks"""
        top_3_common = self.top_emotions_counter.most_common(3)
        total_chunks = sum(self.top_emotions_counter.values())
        
        return [
            {"name": name, "frequency": count / total_chunks}
            for name, count in top_3_common
        ]
    

# Updated WebSocket route for audio analysis with authentication
@app.websocket("/ws/analyze-audio")
async def websocket_analyze_audio(websocket: WebSocket):
    await websocket.accept()
    
    try:
        # Receive the token
        token_data = await websocket.receive_json()
        token = token_data.get("token")
        
        if not token:
            await websocket.send_json({"error": "Authentication token is required"})
            await websocket.close()
            return

        try:
            current_user = await get_current_user(token)
        except HTTPException:
            await websocket.send_json({"error": "Invalid or expired token"})
            await websocket.close()
            return

        processor = AudioChunkProcessor()

        # Receive the audio file through WebSocket
        data = await websocket.receive_bytes()
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_file.write(data)
            temp_file_path = temp_file.name
        
        # Split audio into chunks
        chunks = processor.split_audio(temp_file_path)
        
        # Process each chunk
        async with websockets.connect(HUME_WEBSOCKET_URL) as hume_ws:
            for i, chunk in enumerate(chunks):
                start_time = i * processor.chunk_size_ms / 1000  # Convert to seconds
                chunk_result = await processor.process_chunk(chunk, start_time, hume_ws)
                
                if chunk_result:
                    # Send intermediate results
                    await websocket.send_json({
                        "type": "chunk_result",
                        "chunk": i + 1,
                        "total_chunks": len(chunks),
                        "emotions": chunk_result
                    })
        
        # Send final results
        final_result = {
            "type": "final_result",
            "segment_emotions": processor.segments_emotions,
            "overall_emotions": processor.get_overall_emotions(),
            "most_common_top_emotions": processor.get_most_common_top_emotions()
        }
        await websocket.send_json(final_result)
        
        # Cleanup
        os.unlink(temp_file_path)
                
        
    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
    
    finally:
        await websocket.close()



# Updated REST endpoint for audio upload with authentication
@app.post("/upload-audio")
async def upload_audio(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    if not file.filename.endswith('.mp3'):
        return JSONResponse(
            status_code=400,
            content={"error": "Only MP3 files are supported"}
        )
    
    try:
        processor = AudioChunkProcessor()
        # Save uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Split and process chunks
        chunks = processor.split_audio(temp_file_path)
        
        async with websockets.connect(HUME_WEBSOCKET_URL) as websocket:
            for i, chunk in enumerate(chunks):
                start_time = i * processor.chunk_size_ms / 1000
                chunk_result = await processor.process_chunk(chunk, start_time, websocket)
                if chunk_result:
                    processor.segments_emotions.extend(chunk_result)
        
        result = {
            "segment_emotions": processor.segments_emotions,
            "overall_emotions": processor.get_overall_emotions(),
            "most_common_top_emotions": processor.get_most_common_top_emotions()
        }
        
        # Cleanup
        os.unlink(temp_file_path)
        
        return JSONResponse(status_code=200, content=result)
        
    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred: {str(e)}"}
        )
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)