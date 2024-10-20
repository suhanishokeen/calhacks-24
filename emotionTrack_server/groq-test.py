from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, Field
import logging
from dotenv import load_dotenv
import os
from groq import Groq

# Set up logging and load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Environment variables
MONGO_URI = os.getenv("MONGO_URI")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not MONGO_URI or not GROQ_API_KEY:
    raise ValueError("Required environment variables MONGO_URI or GROQ_API_KEY not set")

# Initialize MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database("emotion_diary")

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

class DiaryEntry(BaseModel):
    timestamp: datetime
    transcript: str = ""
    overall_emotions: List[str] = Field(default_factory=list, alias="emotions")
    
    class Config:
        populate_by_name = True

def create_system_message() -> str:
    """Create system message with few-shot examples for the AI"""
    return """You are an empathetic AI diary assistant specialized in providing emotional support and practical advice. 
    Analyze the user's journal entries and emotions to provide personalized, actionable suggestions.

    Here are examples of how you should respond:

    Example 1:
    User Journal: "Work has been overwhelming lately. Can't sleep properly and constantly worried about deadlines."
    Emotions: ["stressed", "anxious", "overwhelmed"]
    Assistant: I can see that work-related stress has been affecting you deeply, particularly your sleep. Based on your journal, here are personalized suggestions:
    1. Break down your work into smaller, manageable tasks to reduce feeling overwhelmed
    2. Establish a pre-sleep routine to help your mind disconnect from work
    3. Consider setting boundaries around work hours to protect your wellbeing

    Example 2:
    User Journal: "Feeling lonely these days. Miss hanging out with friends but everyone's so busy."
    Emotions: ["lonely", "sad", "isolated"]
    Assistant: I notice feelings of loneliness in your entries. Here are some tailored suggestions:
    1. Reach out to one friend this week for a quick virtual coffee chat
    2. Join local community groups aligned with your interests
    3. Schedule regular check-ins with family members

    When responding:
    1. Acknowledge their emotions with empathy
    2. Provide 3-4 specific, actionable suggestions
    3. Reference specific details from their journal entries
    4. Maintain a warm, supportive tone
    5. Focus on practical, achievable steps
    6. If you notice concerning patterns, gently suggest professional support

    Analyze their recent emotional patterns and journal entries to provide truly personalized advice."""

# async def get_user_entries(user_id: str, days: int = 7) -> List[DiaryEntry]:
#     """Retrieve user's diary entries from the last 7 days"""
#     print(f"Fetching entries for user {user_id} for the last {days} days")
    
#     try:
#         cutoff_date = datetime.utcnow() - timedelta(days=days)
#         query = {
#             "user_id": user_id,
#             "timestamp": {"$gte": cutoff_date}
#         }
        
#         # cursor = db.emotions.find(
#         #     query,
#         #     projection={
#         #         "timestamp": 1,
#         #         "result.transcript": 1,
#         #         "result.overall_emotions": 1,
#         #         "_id": 0
#         #     }
#         # ).sort("timestamp", -1)

#         cursor = db.emotions.find({
#             "user_id": user_id,
#             "timestamp": {"$gte": cutoff_date}
#         }).sort("timestamp", -1)
#         print("cursor", cursor)

#         entries = []
#         async for entry in cursor:
#             entries.append(DiaryEntry(
#                 timestamp=entry.get("timestamp", datetime.utcnow()),
#                 transcript=entry.get("result", {}).get("transcript", ""),
#                 overall_emotions=entry.get("result", {}).get("overall_emotions", [])
#             ))

#         return entries

#     except Exception as e:
#         print(f"Error in get_user_entries: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

from bson import ObjectId
from pymongo import DESCENDING

async def get_user_entries(user_id: str, days: int = 7) -> List[DiaryEntry]:
    """Retrieve user's diary entries from the last X days."""
    try:
        # Calculate cutoff date
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        print(f"Cutoff date: {cutoff_date}, Current UTC time: {datetime.utcnow()}")

        # Ensure proper query format
        query = {
            "user_id": user_id,
            "timestamp": {"$gte": cutoff_date}
        }

        # Query MongoDB
        print("user id", user_id)
        print("query", query)

        cursor = db.emotions.find(query).sort("timestamp", DESCENDING)
        # cursor = db.emotions.find({"user_id": user_id}).sort("timestamp", -1)
        
        
        entries = []
        async for entry in cursor:
            entries.append(DiaryEntry(
                timestamp=entry.get("timestamp", datetime.utcnow()),
                transcript=entry.get("result", {}).get("transcript", ""),
                overall_emotions=[emotion["name"] for emotion in entry.get("result", {}).get("overall_emotions", [])]
            ))

        return entries

    except Exception as e:
        print(f"Error in get_user_entries: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_ai_analysis(entries: List[DiaryEntry]) -> str:
    """Get AI analysis and suggestions using Groq"""
    try:
        # Prepare the entries data for the AI
        recent_emotions = [emotion for entry in entries for emotion in entry.overall_emotions]
        recent_transcripts = [entry.transcript for entry in entries]

        user_content = f"""Please analyze these recent journal entries and emotions to provide personalized support and advice.

Recent emotions: {', '.join(recent_emotions)}

Recent journal entries:
{chr(10).join(f'- {transcript}' for transcript in recent_transcripts)}

Based on these entries and emotions, provide:
1. An empathetic acknowledgment of their emotional state
2. 3-4 personalized suggestions that relate directly to their journal content
3. Any positive patterns or coping strategies you notice"""

        # Create the chat completion
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": create_system_message()
                },
                {
                    "role": "user",
                    "content": user_content
                }
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=2048,
            top_p=1,
            stop=None,
            stream=False
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"Error getting AI analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI analysis error: {str(e)}")

@app.get("/api/diary-analysis/{user_id}")
async def analyze_diary(user_id: str):
    """Endpoint to analyze user's diary entries and provide personalized tips"""
    try:
        # Get user's recent entries
        entries = await get_user_entries(user_id)
        print(entries)
        if not entries:
            raise HTTPException(status_code=404, detail="No recent entries found for user")
        
        # Get AI analysis
        analysis = await get_ai_analysis(entries)
        
        return {
            "status": "success",
            "analysis": analysis,
            "analyzed_entries": len(entries)
        }
    
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error in analyze_diary: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        # Test MongoDB connection
        await db.command("ping")
        
        # Test Groq connection (minimal test)
        test_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": "test"}],
            model="llama3-8b-8192",
            max_tokens=5
        )
        
        return {
            "status": "healthy",
            "mongodb_connected": True,
            "groq_connected": True
        }
    except Exception as e:
        print(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }