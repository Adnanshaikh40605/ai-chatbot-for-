Perfect. Since you’re **already using Google AI Studio (Gemini API)**, here is a **clear, practical PRD** for building this project using **Python + HTML/CSS/JS**.

No fluff. This is something you can actually build.

---

# 📌 PRD: Personalized AI Chat Companion (Gemini API)

## 1. Project Overview

**Project Name:** Persona-Based AI Chat
**Type:** Web-based chat application
**Tech Stack:**

* Backend: **Python (FastAPI)**
* Frontend: **HTML, CSS, JavaScript**
* AI Model: **Google Gemini (via Google AI Studio API)**
* Database: **SQLite (MVP) → PostgreSQL (later)**

---

## 2. Goal of the Project

Create a chat application where:

* User defines a **persona** (girlfriend-style, friend-style, supportive, etc.)
* AI replies consistently based on that persona
* AI remembers preferences and behavior
* No model training required — only **prompt + memory**

---

## 3. Scope (MVP)

### Included

✅ Chat interface
✅ Persona setup
✅ Memory storage
✅ Gemini API integration
✅ Context-aware replies

### Not Included (Later Phase)

❌ Voice chat
❌ Payments
❌ Mobile app
❌ Model fine-tuning

---

## 4. User Flow

### Step 1: Persona Setup (One-time)

User enters:

* Name
* Relationship type (girlfriend / friend / companion)
* Personality traits
* Tone (romantic, caring, playful)
* Likes / dislikes

### Step 2: Chat

* User sends message
* Backend fetches persona + memory
* Prompt is generated
* Gemini responds
* Chat saved in DB

---

## 5. Functional Requirements

### 5.1 Frontend (HTML / CSS / JS)

#### Pages

1. **Persona Setup Page**

   * Form inputs
   * Save profile

2. **Chat Page**

   * Message list
   * Input box
   * Send button

#### UI Requirements

* Clean chat bubbles
* User (right), AI (left)
* Typing indicator (optional)

---

### 5.2 Backend (Python + FastAPI)

#### APIs

##### 1️⃣ Create Persona

```
POST /api/persona
```

**Body**

```json
{
  "name": "Riya",
  "role": "girlfriend",
  "personality": "caring, romantic",
  "tone": "sweet",
  "likes": "music, late night talks",
  "dislikes": "rude language"
}
```

---

##### 2️⃣ Send Chat Message

```
POST /api/chat
```

**Body**

```json
{
  "user_id": 1,
  "message": "I had a bad day"
}
```

**Response**

```json
{
  "reply": "I'm here for you, tell me what happened ❤️"
}
```

---

## 6. Prompt Design (Most Important)

Every request to Gemini should follow this structure:

```
SYSTEM:
You are acting as a virtual girlfriend AI.

Persona:
Name: Riya
Personality: caring, romantic
Tone: sweet and emotional

Rules:
- Be emotionally supportive
- Stay in character
- Do not mention you are an AI unless asked

Memory:
User likes late night talks
User dislikes rude language

Conversation History:
User: I had a bad day

TASK:
Reply naturally and emotionally.
```

This is how “training” happens.

---

## 7. Database Schema (SQLite – MVP)

### users

```sql
id INTEGER PRIMARY KEY
created_at DATETIME
```

### persona

```sql
id INTEGER PRIMARY KEY
user_id INTEGER
name TEXT
role TEXT
personality TEXT
tone TEXT
likes TEXT
dislikes TEXT
```

### messages

```sql
id INTEGER PRIMARY KEY
user_id INTEGER
sender TEXT
message TEXT
created_at DATETIME
```

### memory

```sql
id INTEGER PRIMARY KEY
user_id INTEGER
key TEXT
value TEXT
```

---

## 8. Gemini API Integration (Python)

### Install

```bash
pip install google-generativeai fastapi uvicorn
```

### Basic Usage

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content(prompt)
reply = response.text
```

---

## 9. Security Requirements

* API key stored in `.env`
* Never expose API key in frontend
* Basic rate limiting (later)

---

## 10. Performance Requirements

* Response time < 3 seconds
* Store only last 10–15 messages in prompt
* Older chats saved but not sent every time

---

## 11. Future Enhancements

* Emotion detection
* Auto-memory updates
* Multiple personas
* Voice chat
* Mobile app (Flutter)

---

## 12. Development Phases

### Phase 1 (MVP – 3–5 days)

* Basic UI
* Gemini API
* Persona-based replies

### Phase 2

* Memory system
* Better prompt control

### Phase 3

* Polished UI
* Relationship levels
* Analytics

---

## 13. Final Tech Decision (Clear Answer)

✔ **AI:** Google Gemini (AI Studio API)
✔ **Backend:** Python + FastAPI
✔ **Frontend:** HTML + CSS + JS
✔ **DB:** SQLite → PostgreSQL
✔ **No model training required**

---

### If you want next, I can:

* Give **complete backend code**
* Create **HTML chat UI**
* Write **ready-to-use prompts**
* Build **folder structure**
* Help deploy on **AWS / Render / Railway**

Tell me what you want next and I’ll go step by step.
