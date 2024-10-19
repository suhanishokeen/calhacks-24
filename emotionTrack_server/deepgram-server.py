import os 
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
VOICE_AGENT_URL = "wss://agent.deepgram.com/agent"
USER_AUDIO_SAMPLE_RATE = 16000

# Deepgram settings
SETTINGS = {
    "type": "SettingsConfiguration",
    "audio": {
        "input": {
            "encoding": "linear16",
            "sample_rate": USER_AUDIO_SAMPLE_RATE,
        },
        "output": {
            "encoding": "linear16",
            "sample_rate": USER_AUDIO_SAMPLE_RATE,
            "container": "none",
        },
    },
    "agent": {
        "listen": {"model": "nova-2"},
        "think": {
            "provider": {"type": "open_ai"},
            "model": "gpt-4o-mini",
            "instructions": "You are a helpful assistant.",
        },
        "speak": {"model": "aura-asteria-en"},
    },
}