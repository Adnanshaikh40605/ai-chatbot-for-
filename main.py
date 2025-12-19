from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import init_db, get_db
from models import User, Persona, Message
from schemas import PersonaCreate, PersonaResponse, ChatRequest, ChatResponse, UserResponse
from ai_service import GeminiAI
import os

app = FastAPI(title="Persona-Based AI Chat")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# AI service will be initialized lazily
_ai_service = None

def get_ai_service():
    global _ai_service
    if _ai_service is None:
        _ai_service = GeminiAI()
    return _ai_service

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root():
    """Serve the main HTML page"""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "API is running. Frontend not found."}


@app.post("/api/user", response_model=UserResponse)
async def create_user(db: Session = Depends(get_db)):
    """Create a new user"""
    user = User()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/api/persona", response_model=PersonaResponse)
async def create_persona(persona_data: PersonaCreate, db: Session = Depends(get_db)):
    """Create or update persona for a user"""
    # Check if user exists
    user = db.query(User).filter(User.id == persona_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if persona already exists
    existing_persona = db.query(Persona).filter(Persona.user_id == persona_data.user_id).first()
    if existing_persona:
        # Update existing persona
        existing_persona.name = persona_data.name
        existing_persona.role = persona_data.role
        existing_persona.personality = persona_data.personality
        existing_persona.tone = persona_data.tone
        existing_persona.likes = persona_data.likes
        existing_persona.dislikes = persona_data.dislikes
        db.commit()
        db.refresh(existing_persona)
        return existing_persona
    
    # Create new persona
    persona = Persona(**persona_data.dict())
    db.add(persona)
    db.commit()
    db.refresh(persona)
    return persona


@app.get("/api/persona/{user_id}", response_model=PersonaResponse)
async def get_persona(user_id: int, db: Session = Depends(get_db)):
    """Get persona for a user"""
    persona = db.query(Persona).filter(Persona.user_id == user_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    return persona


@app.post("/api/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest, db: Session = Depends(get_db)):
    """Send a chat message and get AI response"""
    try:
        service = get_ai_service()
        reply = service.chat(db, chat_request.user_id, chat_request.message)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/chat/history/{user_id}")
async def get_chat_history(user_id: int, limit: int = 50, db: Session = Depends(get_db)):
    """Get chat history for a user"""
    messages = db.query(Message).filter(
        Message.user_id == user_id
    ).order_by(Message.created_at.desc()).limit(limit).all()
    
    return [{
        "id": msg.id,
        "sender": msg.sender,
        "message": msg.message,
        "created_at": msg.created_at.isoformat()
    } for msg in reversed(messages)]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
