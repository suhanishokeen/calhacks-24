from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.responses import JSONResponse
import base64
from pathlib import Path
import asyncio
import json
import websockets
import tempfile
import os
from pydub import AudioSegment
from collections import defaultdict, Counter
import statistics
from typing import List, Dict, Any
import logging


app = FastAPI()
HUME_API_KEY = "cA4UwmmxaQ0GzIwfriZontAeewATKGIX4z5xHDy5mKRq9WRJ"
HUME_WEBSOCKET_URL = f"wss://api.hume.ai/v0/stream/models?apikey={HUME_API_KEY}"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# @app.websocket("/ws/analyze-audio")
# async def websocket_analyze_audio(websocket: WebSocket):
#     await websocket.accept()
#     processor = AudioChunkProcessor()
    
#     try:
#         # Receive the audio file through WebSocket
#         data = await websocket.receive_bytes()
        
#         # Save to temporary file
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
#             temp_file.write(data)
#             temp_file_path = temp_file.name
        
#         # Split audio into chunks
#         chunks = processor.split_audio(temp_file_path)
        
#         # Process each chunk
#         async with websockets.connect(HUME_WEBSOCKET_URL) as hume_ws:
#             for i, chunk in enumerate(chunks):
#                 start_time = i * processor.chunk_size_ms / 1000  # Convert to seconds
#                 chunk_result = await processor.process_chunk(chunk, start_time, hume_ws)
                
#                 if chunk_result:
#                     # Send intermediate results
#                     await websocket.send_json({
#                         "type": "chunk_result",
#                         "chunk": i + 1,
#                         "total_chunks": len(chunks),
#                         "emotions": chunk_result
#                     })
        
#         # Send final results
#         final_result = {
#             "type": "final_result",
#             "segment_emotions": processor.segments_emotions,
#             "overall_emotions": processor.get_overall_emotions(),
#             "most_common_top_emotions": processor.get_most_common_top_emotions()
#         }
#         await websocket.send_json(final_result)
        
#         # Cleanup
#         os.unlink(temp_file_path)
        
#     except Exception as e:
#         logger.error(f"Error processing audio: {str(e)}")
#         await websocket.send_json({
#             "type": "error",
#             "message": str(e)
#         })
    
#     finally:
#         await websocket.close()

# # Optional REST endpoint for testing
# @app.post("/upload-audio")
# async def upload_audio(file: UploadFile = File(...)):
#     if not file.filename.endswith('.mp3'):
#         return JSONResponse(
#             status_code=400,
#             content={"error": "Only MP3 files are supported"}
#         )
    
#     try:
#         processor = AudioChunkProcessor()
        
#         # Save uploaded file
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
#             content = await file.read()
#             temp_file.write(content)
#             temp_file_path = temp_file.name
        
#         # Split and process chunks
#         chunks = processor.split_audio(temp_file_path)
        
#         async with websockets.connect(HUME_WEBSOCKET_URL) as websocket:
#             for i, chunk in enumerate(chunks):
#                 start_time = i * processor.chunk_size_ms / 1000
#                 chunk_result = await processor.process_chunk(chunk, start_time, websocket)
#                 if chunk_result:
#                     processor.segments_emotions.extend(chunk_result)
        
#         result = {
#             "segment_emotions": processor.segments_emotions,
#             "overall_emotions": processor.get_overall_emotions(),
#             "most_common_top_emotions": processor.get_most_common_top_emotions()
#         }
        
#         # Cleanup
#         os.unlink(temp_file_path)
        
#         return JSONResponse(status_code=200, content=result)
        
#     except Exception as e:
#         logger.error(f"Error processing audio: {str(e)}")
#         return JSONResponse(
#             status_code=500,
#             content={"error": f"An error occurred: {str(e)}"}
#         )