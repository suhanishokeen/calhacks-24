from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import httpx
from typing import List, Dict
import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

# MongoDB connection
MONGODB_URL = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.emotion_diary

# Groq API settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/v1/completions"

class DiaryEntry(BaseModel):
    timestamp: datetime
    transcript: str = ""
    overall_emotions: List[str] = Field(default_factory=list, alias="emotions")



async def test_mongodb_connection(db) -> bool:
    """Test if MongoDB connection is working"""
    try:
        # Ping the database
        await db.command('ping')
        return True
    except Exception as e:
        print(f"MongoDB connection test failed: {str(e)}")
        return False
    

async def get_user_entries(user_id: str, days: int = 7) -> List[DiaryEntry]:
    """Retrieve user's diary entries from the last 7 days"""
    print("inside get_user_entries")
    
    connection_ok = await test_mongodb_connection(db)
    if not connection_ok:
        raise HTTPException(status_code=500, detail="Database connection error")

    cutoff_date = datetime.utcnow() - timedelta(days=days)
    cursor = db.emotions.find({
        "user_id": user_id,
        "timestamp": {"$gte": cutoff_date}
    }).sort("timestamp", -1)
    print("cursor created")
    
    entries = []
    print("cursor", cursor)
    async for entry in cursor:
        print("inside async for")
        entries.append(DiaryEntry(timestamp=entry["timestamp"],transcript=entry.get("transcript", ""), emotions=entry.get("overall_emotions", [])
        ))
    
    print(f"Total entries retrieved: {len(entries)}")

    return entries

def create_prompt(entries: List[DiaryEntry]) -> str:
    """Create a personalized prompt for the AI based on user's entries"""
    
    # Example prompts for few-shot learning
    few_shot_examples = """
Example 1:
User entries show: Anxiety, stress about work
Response: I notice you've been experiencing anxiety related to work. Here are personalized suggestions:
1. Consider breaking large tasks into smaller, manageable chunks
2. Try the 5-4-3-2-1 grounding technique when feeling overwhelmed
3. Based on your journals, morning times seem to be when you're most productive - try tackling important tasks then

Example 2:
User entries show: Loneliness, social isolation
Response: I've noticed themes of loneliness in your recent entries. Here are tailored suggestions:
1. You mentioned enjoying painting last week - consider joining a local art class
2. Schedule regular video calls with friends/family
3. Based on your entries, you feel better after outdoor activities - try joining a walking group
"""

    # Compile recent emotions and transcripts
    recent_emotions = [emotion for entry in entries for emotion in entry.overall_emotions]
    recent_transcripts = [entry.transcript for entry in entries]
    
    main_prompt = f"""
You are an empathetic AI diary assistant. Analyze the following user's journal entries and emotions to provide personalized, actionable advice. Be warm and supportive, but practical.

Recent emotions: {', '.join(recent_emotions)}
Recent journal entries: {' | '.join(recent_transcripts[:7])}

Based on the user's actual experiences and patterns from their journal entries, provide:
1. A brief, empathetic acknowledgment of their emotional state
2. 3-4 personalized suggestions that directly relate to their entries
3. Point out any positive patterns or coping strategies they've mentioned before

{few_shot_examples}

Provide your response in a conversational, caring tone:
"""
    return main_prompt

async def get_ai_response(prompt: str) -> str:
    """Get response from Groq API"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama3-groq-70b-8192-tool-use-preview",  # or your preferred Groq model
        "messages": [
            {"role": "system", "content": "You are an empathetic AI diary assistant providing personalized emotional support and practical advice."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 3000
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_API_URL, json=data, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error getting AI response")
        return response.json()["choices"][0]["message"]["content"]


from groq import Groq

client = Groq()

chat_completion = client.chat.completions.create(
    #
    # Required parameters
    #
    messages=[
        # Set an optional system message. This sets the behavior of the
        # assistant and can be used to provide specific instructions for
        # how it should behave throughout the conversation.
        {
            "role": "system",
            "content": "you are a helpful assistant."
        },
        # Set a user message for the assistant to respond to.
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],

    # The language model which will generate the completion.
    model="llama3-8b-8192",

    temperature=0.5,
    max_tokens=2048,
    top_p=1,
    stop=None,
    stream=False,
)

# Print the completion returned by the LLM.
print(chat_completion.choices[0].message.content)

@app.get("/api/diary-analysis/{user_id}")
async def analyze_diary(user_id: str):
    """Endpoint to analyze user's diary entries and provide personalized tips"""
    try:
        # Get user's recent entries
        entries = await get_user_entries(user_id)

        print("retreived user entries")
        if not entries:
            raise HTTPException(status_code=404, detail="No recent entries found for user")
        
        # Create prompt based on entries
        prompt = create_prompt(entries)
        print("prompt created")
        # Get AI response
        ai_response = await get_ai_response(prompt)
        print("retrieved ai response")

        return {
            "status": "success",
            "response": ai_response,
            "analyzed_entries": len(entries),
            "date_range": f"Last {7} days"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)