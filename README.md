# 🤖 Persona-Based AI Chat Companion

A modern web application that lets you create personalized AI companions with unique personalities, powered by Google's Gemini AI.

## ✨ Features

- **Personalized AI Personas**: Create AI companions with custom names, roles, personalities, and communication tones
- **Context-Aware Conversations**: AI remembers conversation history and responds based on your persona's traits
- **Beautiful UI**: Premium dark theme with smooth animations and glassmorphism effects
- **Real-time Chat**: Interactive messaging with typing indicators
- **Persistent Memory**: Chat history saved and retrieved across sessions

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))

### Installation

1. **Install Dependencies** (no virtual environment as requested):
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   - Open the `.env` file
   - Replace `your_api_key_here` with your actual Gemini API key:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     ```

3. **Run the Application**:
   ```bash
   python main.py
   ```

4. **Open in Browser**:
   - Navigate to `http://localhost:8000`
   - Create your AI companion and start chatting!

## 📁 Project Structure

```
pop bna/
├── main.py              # FastAPI server and API endpoints
├── ai_service.py        # Gemini AI integration and prompt building
├── models.py            # Database models (User, Persona, Message, Memory)
├── database.py          # Database configuration
├── schemas.py           # Pydantic validation schemas
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (API keys)
├── static/
│   ├── index.html       # Main HTML interface
│   ├── style.css        # Styling and animations
│   └── script.js        # Frontend logic and API calls
└── chat.db              # SQLite database (auto-created)
```

## 🎨 Persona Customization

When creating your AI companion, you can customize:

- **Name**: Give your companion a unique name
- **Role**: Choose from girlfriend, boyfriend, friend, companion, or mentor
- **Personality**: Define personality traits (e.g., "caring, romantic, playful")
- **Tone**: Select communication style (sweet, playful, caring, romantic, casual, professional)
- **Likes/Dislikes**: Add preferences to personalize responses further

## 🔧 API Endpoints

- `POST /api/user` - Create a new user
- `POST /api/persona` - Create or update persona
- `GET /api/persona/{user_id}` - Get persona details
- `POST /api/chat` - Send message and receive AI response
- `GET /api/chat/history/{user_id}` - Retrieve chat history

## 💡 How It Works

1. **Persona Creation**: Your chosen personality traits are stored in the database
2. **Prompt Engineering**: Each message creates a custom prompt with:
   - Persona details (name, role, personality, tone)
   - Conversation history (last 10 messages)
   - User preferences and memories
3. **AI Response**: Gemini AI generates responses that match your persona's personality
4. **Memory**: All messages are saved for context in future conversations

## 🎯 Technology Stack

- **Backend**: Python, FastAPI, SQLAlchemy
- **Frontend**: Vanilla HTML, CSS, JavaScript
- **AI**: Google Gemini 1.5 Flash
- **Database**: SQLite

## 🔒 Security

- API keys stored in `.env` file (never exposed to frontend)
- `.gitignore` configured to exclude sensitive files
- Database file excluded from version control

## 📝 Notes

- No virtual environment used (as requested)
- Chat history persists in local SQLite database
- Frontend uses localStorage for session management

## 🚧 Future Enhancements

- Voice chat capability
- Multiple personas per user
- Emotion detection
- Advanced memory system
- Mobile app version

## 📄 License

MIT License - Feel free to use and modify!

---

**Enjoy chatting with your personalized AI companion! 🎉**
