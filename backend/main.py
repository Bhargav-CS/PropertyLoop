from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import shutil
import os
from agents.router_agent import routeragent

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


# @app.get("/", response_class=HTMLResponse)
# async def serve_homepage():
#     index_path = os.path.join(frontend_path, "index.html")
#     return FileResponse(index_path)

# Payload model for /chat
class ChatRequest(BaseModel):
    text: Optional[str] = None
    image: Optional[str] = None  # base64 string (we’ll decode later)

@app.post("/chat")
async def chat(req: ChatRequest):
    print(f"[INPUT] Text: {req.text}, Image: {'Provided' if req.image else 'Not Provided'}")

    try:
        # Always use the dynamic auto-routing logic
        result = routeragent._auto_route(text=req.text, image_base64=req.image)
        return {"response": result}
    except Exception as e:
        return {"error": str(e)}


