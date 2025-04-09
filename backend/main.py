from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import shutil
import os
import uuid  # Import for generating unique session IDs
from agents.router_agent import routeragent
from agents.faq_agent import run_faq_agent
from agents.vision_agent import run_vision_agent

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend build
frontend_path = os.path.join(os.path.dirname(__file__), "static")

# In-memory storage for chat history
chat_histories = {}

# Payload model for /chat
class ChatRequest(BaseModel):
    text: Optional[str] = None
    image: Optional[str] = None  # base64 string (we’ll decode later)
    session_id: Optional[str] = None  # Optional, generated if not provided

@app.post("/chat")
async def chat(req: ChatRequest):
    print(f"[INPUT] Text: {req.text}, Image: {'Provided' if req.image else 'Not Provided'}")

    # Generate a session ID if not provided
    session_id = req.session_id or str(uuid.uuid4())
    if session_id not in chat_histories:
        chat_histories[session_id] = []

    chat_history = chat_histories[session_id]

    try:
        # Use the router agent to decide which agent to use
        response = routeragent.route(query=req.text or "", image_base64=req.image, chat_history=chat_history)

        # Update chat history
        chat_history.append((req.text or "[Image Provided]", response))

        return {"response": response, "session_id": session_id}
    except Exception as e:
        return {"error": str(e), "session_id": session_id}


