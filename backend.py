# backend.py

from dotenv import load_dotenv
load_dotenv()

import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from langchain_core.messages import HumanMessage, AIMessage
import traceback

# Import the new, simplified functions
from core.services import transcribe_audio, synthesize_speech
from core.graph import get_agent_response, get_final_report

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

conversations = {}

@app.post("/start-interview/{role}")
async def start_interview(role: str):
    conversation_id = str(uuid.uuid4())
    graph_state = {
        "role": role,
        "conversation_history": [AIMessage(content=f"Hello! Welcome to your interview for the {role} position. To begin, can you tell me a little about yourself?")]
    }
    conversations[conversation_id] = graph_state
    
    initial_greeting_text = graph_state["conversation_history"][0].content
    audio_bytes = synthesize_speech(initial_greeting_text)
    
    return Response(content=audio_bytes, media_type="audio/mpeg", headers={"X-Conversation-Id": conversation_id})

@app.post("/process-answer/{conversation_id}")
async def process_answer(conversation_id: str, audio_file: UploadFile = File(...)):
    if conversation_id not in conversations:
        return JSONResponse(status_code=404, content={"message": "Error: Conversation ID not found."})

    try:
        audio_bytes = await audio_file.read()
        user_text = transcribe_audio(audio_bytes)
        
        # --- THIS IS THE NEW, SIMPLER LOGIC ---
        graph_state = conversations[conversation_id]
        graph_state["conversation_history"].append(HumanMessage(content=user_text))
        
        # Check if we should end the interview
        human_message_count = sum(1 for msg in graph_state["conversation_history"] if isinstance(msg, HumanMessage))
        
        if human_message_count >= 3:
            # Generate and send the final report
            print("INFO: Reached 3 user messages. Generating final report.")
            full_report = get_final_report(graph_state["role"], graph_state["conversation_history"])
            del conversations[conversation_id]
            return Response(content=full_report, media_type="text/plain")
        else:
            # Get the next question
            print("INFO: Getting next question from agent.")
            ai_response = get_agent_response(graph_state["role"], graph_state["conversation_history"])
            graph_state["conversation_history"].append(ai_response)
            
            # Synthesize and send the audio
            ai_audio_response = synthesize_speech(ai_response.content)
            return Response(content=ai_audio_response, media_type="audio/mpeg")

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"message": "An internal server error occurred."})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)