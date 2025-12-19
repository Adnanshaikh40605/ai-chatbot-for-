# AI Chatbot - Django REST Framework

A modern, persona-based AI chatbot built with Django REST Framework and Google Gemini AI, featuring a beautiful mobile-first responsive design.

![AI Chatbot](https://img.shields.io/badge/Django-4.2.7-green)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![Gemini](https://img.shields.io/badge/Gemini-2.5--flash--lite-orange)

## ✨ Features

- 🤖 **Personalized AI Companions** - Create custom AI personas with unique personalities
- 📱 **Mobile-First Design** - Beautiful, responsive UI optimized for all devices
- ✅ **Multi-Select Interface** - Quick persona creation with checkbox options
- 💬 **Real-time Chat** - Smooth chat experience with typing indicators
- 🎨 **Modern UI** - Gradient designs, smooth animations, and glassmorphism
- 🔄 **REST API** - Full Django REST Framework backend
- 💾 **Chat History** - Persistent conversation storage

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Google Gemini API Key ([Get one here](https://ai.google.dev/))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Adnanshaikh40605/ai-chatbot-for-.git
cd ai-chatbot-for-
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Start the server**
```bash
python manage.py runserver
```

7. **Open your browser**
```
http://127.0.0.1:8000/
```

## 📖 Usage

### Creating Your AI Companion

1. Fill in the persona form:
   - **Name**: Give your AI a name
   - **Relationship Type**: Choose from girlfriend, boyfriend, friend, companion, or mentor
   - **Personality Traits**: Select multiple traits (caring, romantic, playful, etc.)
   - **Communication Tone**: Choose how your AI communicates
   - **Likes/Dislikes**: Optional preferences

2. Click "Create Companion ✨"

3. Start chatting!

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/users/` | POST | Create new user |
| `/api/personas/` | POST | Create/update persona |
| `/api/personas/{user_id}/` | GET | Get persona details |
| `/api/chat/` | POST | Send message and get AI response |
| `/api/messages/{user_id}/` | GET | Get chat history |

## 🛠️ Tech Stack

### Backend
- **Django 4.2.7** - Web framework
- **Django REST Framework** - API development
- **Google Gemini AI** - AI model (gemini-2.5-flash-lite)
- **SQLite** - Database (development)

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling (Mobile-first, responsive)
- **Vanilla JavaScript** - Interactivity
- **Inter Font** - Typography

## 📱 Mobile Features

- ✅ Touch-friendly UI (44px+ tap targets)
- ✅ Responsive breakpoints (mobile, tablet, desktop)
- ✅ Smooth animations and transitions
- ✅ Keyboard-aware input positioning
- ✅ Pull-to-refresh ready
- ✅ PWA-ready architecture

## 🎨 Design Highlights

- **Color Palette**: Indigo & Purple gradients
- **Animations**: Slide-in messages, bounce typing indicator
- **Components**: Custom modal popups, checkbox groups
- **Accessibility**: Semantic HTML, ARIA-ready

## 🔧 Configuration

### Changing the AI Model

Edit `chat/gemini_service.py`:
```python
response = self.client.models.generate_content(
    model='gemini-2.5-flash-lite',  # Change model here
    contents=prompt
)
```

Available models:
- `gemini-2.5-flash-lite` - Ultra fast, cost-efficient
- `gemini-2.5-flash` - Balanced performance
- `gemini-2.5-pro` - Advanced reasoning

## 📝 Project Structure

```
ai-chatbot-for-/
├── chat/                   # Main Django app
│   ├── models.py          # Database models
│   ├── serializers.py     # REST serializers
│   ├── views.py           # API views
│   ├── gemini_service.py  # AI integration
│   └── urls.py            # App URLs
├── config/                # Django settings
│   ├── settings.py
│   └── urls.py
├── static/                # Static files
│   ├── css/
│   │   └── mobile-first.css
│   └── js/
│       └── app.js
├── templates/             # HTML templates
│   └── index.html
├── manage.py
└── requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Adnan Shaikh**
- GitHub: [@Adnanshaikh40605](https://github.com/Adnanshaikh40605)

## 🙏 Acknowledgments

- Google Gemini AI for the powerful language model
- Django & DRF communities for excellent documentation
- Inter font by Rasmus Andersson

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

Made with ❤️ using Django and Gemini AI
