from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer,  OAuth2PasswordRequestForm
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
from bson import ObjectId  # Add this import
from fastapi import Query
from typing import Dict, List, Tuple
import statistics
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
import aiofiles  # For making asynchronous HTTP requests


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

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
if not DEEPGRAM_API_KEY:
    raise ValueError("No DEEPGRAM_API_KEY set for Deepgram")

deepgram = DeepgramClient(DEEPGRAM_API_KEY)


# Pydantic models
class User(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str

class TokenWithUser(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse

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

# Add this function if it's not already present
async def authenticate_user(email: str, password: str):
    user = await db.users.find_one({"email": email})
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user

# Helper function to convert ObjectId to string
def serialize_dict(obj: Dict[str, Any]) -> Dict[str, Any]:
    """Convert any ObjectId in a dictionary to string"""
    for key, value in obj.items():
        if isinstance(value, ObjectId):
            obj[key] = str(value)
        elif isinstance(value, dict):
            obj[key] = serialize_dict(value)
        elif isinstance(value, list):
            obj[key] = [
                serialize_dict(item) if isinstance(item, dict) 
                else str(item) if isinstance(item, ObjectId)
                else item 
                for item in value
            ]
    return obj

# Helper function to serialize MongoDB documents
def serialize_mongodb_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert MongoDB document to JSON serializable format"""
    if doc is None:
        return None
    
    result = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            result[key] = str(value)
        elif isinstance(value, dict):
            result[key] = serialize_mongodb_doc(value)
        elif isinstance(value, list):
            result[key] = [
                serialize_mongodb_doc(item) if isinstance(item, dict)
                else str(item) if isinstance(item, ObjectId)
                else item
                for item in value
            ]
        else:
            result[key] = value
    return result

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if user is None:
            raise credentials_exception
        return serialize_mongodb_doc(user)
    except (JWTError, Exception) as e:
        print(f"An error occurred: {e}")
        raise credentials_exception



# Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to the Emotion Diary Backend!"}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user["_id"])}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


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
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )    
    try:
        access_token = create_access_token(data={"sub": str(db_user["_id"])})
        refresh_token = create_refresh_token(data={"sub": str(db_user["_id"])})
        # Prepare user data to return, exclude password
        user_data = UserResponse(
            id=str(db_user["_id"]),
            username=db_user["username"],
            email=db_user["email"]
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user_data
        }
    
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
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        # Verify user exists
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if user is None:
            raise credentials_exception
        # Generate a new access token
        new_access_token = create_access_token({"sub": user_id})
        return {
            "access_token": new_access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except JWTError as e:
        print(f"Error decoding JWT: {e}")
        raise credentials_exception
    except Exception as e:
        print(f"Error refreshing access token: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not refresh access token")



# Improved error handling: Using logging for errors and exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    print(f"An error occurred: {exc}")
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# Protected route
@app.get("/protected/")
async def protected_route(current_user: dict = Depends(get_current_user)):
    try:
        # User is already serialized by get_current_user
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Access granted",
                "user": current_user
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )

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

        print(json.dumps(result, indent=2))
        
        return self.process_emotions(result, start_time)
    
    def analyze_word_emotions(self) -> List[Tuple[str, str, float]]:
        """
        Analyzes emotions for each word and returns top 3 emotion-word pairs.
        Returns: List of tuples (word, emotion, score)
        """
        # Check if there are words to analyze
        if not self.segments_emotions or 'word' not in self.segments_emotions[0]:
            return []
        # Aggregate emotions per word
        word_emotion_scores = defaultdict(lambda: defaultdict(list))
        
        for segment in self.segments_emotions:
            word = segment['word']
            emotions = segment['emotions']
            
            for emotion in emotions:
                word_emotion_scores[word][emotion['name']].append(emotion['score'])
        
        # Calculate average emotion scores per word
        word_emotions_avg = []
        for word, emotions in word_emotion_scores.items():
            for emotion, scores in emotions.items():
                avg_score = statistics.mean(scores)
                word_emotions_avg.append((word, emotion, avg_score))
        
        # Sort by score and get top 3
        return sorted(word_emotions_avg, key=lambda x: x[2], reverse=True)[:3]
    
    def get_overall_emotions(self) -> List[Dict]:
        overall_emotions = {}
        for emotion, scores in self.all_emotions.items():
            overall_emotions[emotion] = statistics.mean(scores)
        
        top_overall = sorted(
            overall_emotions.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]  # Limit to top 3 emotions
        
        return [
            {"name": name, "score": round(score, 3)}
            for name, score in top_overall
        ]

    
    def get_chunk_word_emotions(self, chunk_result: List[Dict]) -> List[Dict]:
        """Analyze emotions for words in a single chunk"""
        chunk_word_emotions = defaultdict(lambda: defaultdict(list))
        
        for segment in chunk_result:
            word = segment['word']
            for emotion in segment['emotions']:
                chunk_word_emotions[word][emotion['name']].append(emotion['score'])
        
        # Get top emotions for this chunk
        chunk_top_emotions = []
        for word, emotions in chunk_word_emotions.items():
            for emotion, scores in emotions.items():
                avg_score = statistics.mean(scores)
                chunk_top_emotions.append({
                    "word": word,
                    "emotion": emotion,
                    "score": avg_score
                })
        
        return sorted(chunk_top_emotions, key=lambda x: x['score'], reverse=True)[:3]


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
    
    def get_overall_emotions_weighted(self) -> List[Dict]:
        """Calculate overall emotions using weighted average"""
        overall_emotions = {}
        total_weight = 0
        for emotion, scores in self.all_emotions.items():
            weight = sum(scores)
            total_weight += weight
            overall_emotions[emotion] = weight
        
        # Normalize the scores
        for emotion in overall_emotions:
            overall_emotions[emotion] /= total_weight
        
        # Get top 3 emotions by weighted score
        top_overall = sorted(
            overall_emotions.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        return [
            {"name": name, "score": round(score, 3)}
            for name, score in top_overall
        ]
        
    def get_emotion_frequencies(self) -> List[Dict]:
        emotion_counts = Counter()
        for emotions in self.all_emotions.values():
            emotion_counts.update(emotions)
        
        total_counts = sum(emotion_counts.values())
        emotion_frequencies = [
            {"name": emotion, "frequency": count / total_counts}
            for emotion, count in emotion_counts.most_common(3)
        ]
        return emotion_frequencies


@app.websocket("/ws/analyze-audio")
async def websocket_analyze_audio(websocket: WebSocket, token: str = Query(None)):
    if not token:
        await websocket.accept()
        await websocket.send_json({"error": "Authentication token is required"})
        await websocket.close()
        return

    try:
        current_user = await get_current_user(token)
        user_id = str(current_user['_id'])
        await websocket.accept()

    except HTTPException as he:
        await websocket.accept()
        await websocket.send_json({"error": he.detail})
        await websocket.close()
    except Exception as e:
        await websocket.accept()
        await websocket.send_json({"error": str(e)})
        await websocket.close()

    await websocket.accept()

    try:
        processor = AudioChunkProcessor()

        # Receive the audio file through WebSocket
        data = await websocket.receive_bytes()
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_file.write(data)
            temp_file_path = temp_file.name
        
        # Split audio into chunks
        chunks = processor.split_audio(temp_file_path)
        
        total_chunks = len(chunks)
        processed_chunks = 0
        
        async with websockets.connect(HUME_WEBSOCKET_URL) as hume_ws:
            for i, chunk in enumerate(chunks):
                start_time = i * processor.chunk_size_ms / 1000
                chunk_result = await processor.process_chunk(chunk, start_time, hume_ws)
                
                if chunk_result:
                    processed_chunks += 1
                    processor.segments_emotions.extend(chunk_result)
                    
                    # Analyze emotions for this chunk
                    chunk_top_emotions = processor.get_chunk_word_emotions(chunk_result)
                    
                    # Calculate current overall emotions
                    current_overall_emotions = processor.get_overall_emotions()
                    
                    # Send intermediate results
                    intermediate_result = {
                        "type": "chunk_result",
                        "chunk": processed_chunks,
                        "total_chunks": total_chunks,
                        "progress": (processed_chunks / total_chunks) * 100,
                        "chunk_top_emotions": chunk_top_emotions,
                        "current_overall_emotions": current_overall_emotions
                    }
                    await websocket.send_json(serialize_dict(intermediate_result))

        # Get final top emotion-word pairs
        top_emotion_words = processor.analyze_word_emotions()
        
        # Prepare final results
        final_result = {
            "type": "final_result",
            "top_emotion_words": [
                {
                    "word": word,
                    "emotion": emotion,
                    "score": score
                }
                for word, emotion, score in top_emotion_words
            ],
            "overall_emotions": processor.get_overall_emotions(),
            "detailed_segments": processor.segments_emotions
        }

        # Store the emotions data in the database
        emotion_record = {
            'user_id': str(current_user['_id']),
            'timestamp': datetime.utcnow(),
            'result': final_result
        }
        inserted_id = await db.emotions.insert_one(emotion_record)
        
        final_result['record_id'] = str(inserted_id.inserted_id)

        # Send final results
        await websocket.send_json(serialize_dict(final_result))
        
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
        user_id = str(current_user['_id'])

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
        
        # top_emotion_words = processor.analyze_word_emotions()

        # Process with Deepgram to get transcript
        # Initialize Deepgram client
        DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
        if not DEEPGRAM_API_KEY:
            raise ValueError("No DEEPGRAM_API_KEY set for Deepgram")
        
        # Read the audio file
        async with aiofiles.open(temp_file_path, 'rb') as audio_file:
            audio_data = await audio_file.read()
            source = {'buffer': audio_data, 'mimetype': 'audio/mp3'}

        # Set the options for transcription
        options = {
            "punctuate": True,
            "model": "nova",
            # "tier": "enhanced",
            # Add any other options you need
        }

        # Perform the transcription
        # transcript_response = await deepgram.transcription.prerecorded(source, options)
        print("just before the model selection")
        transcript_response = deepgram.listen.prerecorded.v("1").transcribe_file(source, options)
        print("Transcript response:", transcript_response)
        print("model:", options["model"])

        # Extract transcript from the response
        transcript = transcript_response['results']['channels'][0]['alternatives'][0]['transcript']

        # Prepare the result
        result = {
            "transcript": transcript,
            "overall_emotions": processor.get_overall_emotions_weighted(),
            "detailed_segments": processor.segments_emotions
        }

        # Store the emotions data in the database
        emotion_record = {
            'user_id': user_id,  # Convert ObjectId to string
            'timestamp': datetime.utcnow(),
            'result': result
        }
        inserted_id = await db.emotions.insert_one(emotion_record)
        result['record_id'] = str(inserted_id.inserted_id)
        
        os.unlink(temp_file_path)
        
        return JSONResponse(status_code=200, content=serialize_dict(result))
        
    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred: {str(e)}"}
        )
    
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


@app.get("/emotions/history")
async def get_emotions_history(current_user: dict = Depends(get_current_user)):
    # Retrieve emotions from the database for the current user
    emotions_cursor = db.emotions.find({'user_id': str(current_user['_id'])}).sort('timestamp', -1)
    emotions_list = await emotions_cursor.to_list(length=None)
    # Convert ObjectId to string for the response
    for emotion in emotions_list:
        emotion['_id'] = str(emotion['_id'])
    return emotions_list



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)