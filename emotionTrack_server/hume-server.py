from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
import asyncio
from hume import AsyncHumeClient
from hume.expression_measurement.stream import Config
from hume.expression_measurement.stream.socket_client import StreamConnectOptions
from collections import defaultdict
import tempfile
import os
from typing import List, Dict
import statistics

app = FastAPI()

HUME_API_KEY = "cA4UwmmxaQ0GzIwfriZontAeewATKGIX4z5xHDy5mKRq9WRJ"  # Replace with your Hume API key

async def process_audio_file(file_path: str) -> Dict:
    client = AsyncHumeClient(api_key=HUME_API_KEY)
    
    # Configure the prosody model
    model_config = Config(prosody={})
    stream_options = StreamConnectOptions(config=model_config)
    
    # Process the audio file
    async with client.expression_measurement.stream.connect(options=stream_options) as socket:
        result = await socket.send_file(file_path)
        
        # Process segments
        segments_emotions = []
        all_emotions = defaultdict(list)
        
        # Extract emotions from each prediction
        for prediction in result.prosody.predictions:
            # Get emotions for this segment
            emotions = prediction.emotions
            # Sort emotions by score and get top 3
            top_emotions = sorted(emotions, key=lambda x: x.score, reverse=True)[:3]
            
            segment_data = {
                "timestamp": prediction.time.begin,
                "emotions": [
                    {"name": emotion.name, "score": round(emotion.score, 3)}
                    for emotion in top_emotions
                ]
            }
            segments_emotions.append(segment_data)
            
            # Add to overall emotions
            for emotion in emotions:
                all_emotions[emotion.name].append(emotion.score)
        
        # Calculate overall emotions
        overall_emotions = {}
        for emotion, scores in all_emotions.items():
            overall_emotions[emotion] = statistics.mean(scores)
        
        # Get top 3 overall emotions
        top_overall = sorted(
            overall_emotions.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        return {
            "segment_emotions": segments_emotions,
            "overall_emotions": [
                {"name": name, "score": round(score, 3)}
                for name, score in top_overall
            ]
        }

@app.post("/analyze-audio")
async def analyze_audio(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith('.mp3'):
        return JSONResponse(
            status_code=400,
            content={"error": "Only MP3 files are supported"}
        )
    
    try:
        # Create a temporary file to store the uploaded audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            # Write the uploaded file content to the temporary file
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Process the audio file
        result = await process_audio_file(temp_file_path)
        
        # Clean up the temporary file
        os.unlink(temp_file_path)
        
        return JSONResponse(
            status_code=200,
            content=result
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred: {str(e)}"}
        )