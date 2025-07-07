# core/services.py 

from groq import Groq
import os
import pyttsx3
from pathlib import Path

# --- Groq Client Setup for Transcription ---
try:
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in .env file.")
    client = Groq(api_key=groq_api_key)
    print("Groq client for transcription initialized successfully.")
except Exception as e:
    print(f"Error initializing Groq client: {e}")
    client = None

# --- Service Functions ---

def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcribes audio bytes using the ultra-fast Groq API."""
    if not client:
        return "Error: Transcription service (Groq) not available."
    
    print("SERVICES: Transcribing with Groq API...")
    try:
        # Groq's API needs the file data passed in a specific way
        files = {"file": ("audio.mp3", audio_bytes)}
        
        groq_response = client.audio.transcriptions.create(
            file=("audio.mp3", audio_bytes),
            model="whisper-large-v3", # This is the name of the model on Groq's platform
        )
        transcript = groq_response.text
        print(f"SERVICES: Groq transcription successful. Text: '{transcript}'")
        return transcript
    except Exception as e:
        print(f"SERVICES: An error occurred during Groq transcription: {e}")
        return "[Transcription Failed]"

def synthesize_speech(text: str) -> bytes:
    """Synthesizes text into speech using the local pyttsx3 engine."""
    print(f"SERVICES: Synthesizing text: '{text[:40]}...' with pyttsx3...")
    temp_speech_file = "temp_tts_output.mp3"
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if len(voices) > 1: engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 160)
        engine.save_to_file(text, temp_speech_file)
        engine.runAndWait()
        with open(temp_speech_file, "rb") as f:
            audio_bytes = f.read()
        return audio_bytes
    except Exception as e:
        return b''
    finally:
        if os.path.exists(temp_speech_file):
            os.remove(temp_speech_file)