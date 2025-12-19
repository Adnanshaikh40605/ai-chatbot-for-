from google import genai
import os


class GeminiService:
    """Service for interacting with Gemini AI"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            raise ValueError("Please set GEMINI_API_KEY in .env file")
        
        # Set API key as environment variable for the SDK
        os.environ["GOOGLE_API_KEY"] = api_key
        self.client = genai.Client()
    
    def build_prompt(self, persona, conversation_history, memories):
        """Build a comprehensive prompt for the AI"""
        
        # Build conversation history (last 10 messages)
        # Convert QuerySet to list to support negative indexing
        history_list = list(conversation_history)
        recent_messages = history_list[-10:] if len(history_list) > 10 else history_list
        
        history_text = ""
        for msg in recent_messages:
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

{f"Likes: {persona.likes}" if persona.likes else ""}
{f"Dislikes: {persona.dislikes}" if persona.dislikes else ""}

{f"Memory:\\n{memory_text}" if memory_text else ""}

Conversation History:
{history_text}

TASK:
Reply naturally as {persona.name} would, based on the personality and tone described above.
"""
        return prompt
    
    def generate_response(self, prompt):
        """Generate a response using Gemini"""
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"I'm having trouble responding right now. Error: {str(e)}"
    
    def chat(self, user, user_message):
        """Main chat function"""
        from .models import Persona, Message, Memory
        
        # Get persona
        try:
            persona = user.persona
        except Persona.DoesNotExist:
            return "Please set up your persona first!"
        
        # Get conversation history
        conversation_history = Message.objects.filter(user=user).order_by('created_at')
        
        # Get memories
        memories = Memory.objects.filter(user=user)
        
        # Build prompt
        prompt = self.build_prompt(persona, conversation_history, memories)
        
        # Generate response
        ai_response = self.generate_response(prompt)
        
        # Save messages
        Message.objects.create(user=user, sender="user", message=user_message)
        Message.objects.create(user=user, sender="ai", message=ai_response)
        
        return ai_response
