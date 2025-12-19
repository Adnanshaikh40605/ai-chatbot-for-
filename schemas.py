from pydantic import BaseModel
from typing import Optional

class PersonaCreate(BaseModel):
    user_id: int
    name: str
    role: str
    personality: str
    tone: str
    likes: Optional[str] = None
    dislikes: Optional[str] = None

class PersonaResponse(BaseModel):
    id: int
    user_id: int
    name: str
    role: str
    personality: str
    tone: str
    likes: Optional[str]
    dislikes: Optional[str]
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    user_id: int
    message: str

class ChatResponse(BaseModel):
    reply: str

class UserCreate(BaseModel):
    pass

class UserResponse(BaseModel):
    id: int
    
    class Config:
        from_attributes = True
