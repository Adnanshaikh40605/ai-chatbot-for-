from google import genai
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from models import Persona, Message, Memory

load_dotenv()

class GeminiAI:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            raise ValueError("Please set GEMINI_API_KEY in .env file")
        
        # Set API key as environment variable for the SDK
        os.environ["GOOGLE_API_KEY"] = api_key
        self.client = genai.Client()
    
    def build_prompt(self, persona: Persona, conversation_history: list, memories: list) -> str:
        """Build a comprehensive prompt for the AI"""
        
        # Build conversation history (last 10 messages)
        history_text = ""
        for msg in conversation_history[-10:]:
            sender_label = "User" if msg.sender == "user" else persona.name
            history_text += f"{sender_label}: {msg.message}\n"
        
        # Build memory context
        memory_text = ""
        for mem in memories:
            memory_text += f"{mem.key}: {mem.value}\n"
        
        prompt = f"""SYSTEM:
You are acting as a virtual {persona.role} AI.

Persona:
Name: {persona.name}
Personality: {persona.personality}
Tone: {persona.tone}

Rules:
- Be emotionally supportive
- Stay in character
- Do not mention you are an AI unless asked
- Respond naturally and emotionally
- Keep responses conversational and not too long

{"Likes: " + persona.likes if persona.likes else ""}
{"Dislikes: " + persona.dislikes if persona.dislikes else ""}

{("Memory:\\n" + memory_text) if memory_text else ""}

Conversation History:
{history_text}

TASK:
Reply naturally as {persona.name} would, based on the personality and tone described above.
"""
        return prompt
    
    def generate_response(self, prompt: str) -> str:
        """Generate a response using Gemini"""
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"I'm having trouble responding right now. Error: {str(e)}"
    
    def chat(self, db: Session, user_id: int, user_message: str) -> str:
        """Main chat function"""
        # Get persona
        persona = db.query(Persona).filter(Persona.user_id == user_id).first()
        if not persona:
            return "Please set up your persona first!"
        
        # Get conversation history
        conversation_history = db.query(Message).filter(
            Message.user_id == user_id
        ).order_by(Message.created_at).all()
        
        # Get memories
        memories = db.query(Memory).filter(Memory.user_id == user_id).all()
        
        # Build prompt
        prompt = self.build_prompt(persona, conversation_history, memories)
        
        # Generate response
        ai_response = self.generate_response(prompt)
        
        # Save messages
        user_msg = Message(user_id=user_id, sender="user", message=user_message)
        ai_msg = Message(user_id=user_id, sender="ai", message=ai_response)
        
        db.add(user_msg)
        db.add(ai_msg)
        db.commit()
        
        return ai_response
