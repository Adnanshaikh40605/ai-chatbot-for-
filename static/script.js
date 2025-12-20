// API Configuration
const API_BASE_URL = window.location.origin;

// State Management
let currentUserId = null;
let currentPersona = null;

// DOM Elements
const setupScreen = document.getElementById('setupScreen');
const chatScreen = document.getElementById('chatScreen');
const personaForm = document.getElementById('personaForm');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const messagesContainer = document.getElementById('messagesContainer');
const typingIndicator = document.getElementById('typingIndicator');
const resetBtn = document.getElementById('resetBtn');

// Initialize App
async function initApp() {
    // Check if user data exists in localStorage
    const savedUserId = localStorage.getItem('userId');
    const savedPersona = localStorage.getItem('persona');

    if (savedUserId && savedPersona) {
        currentUserId = parseInt(savedUserId);
        currentPersona = JSON.parse(savedPersona);
        showChatScreen();
        await loadChatHistory();
    } else {
        // Create a new user
        await createNewUser();
    }
}

// Create New User
async function createNewUser() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/user`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await response.json();
        currentUserId = data.id;
        localStorage.setItem('userId', currentUserId);
    } catch (error) {
        console.error('Error creating user:', error);
        alert('Failed to create user. Please check if the server is running.');
    }
}

// Persona Form Submission
personaForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const personaData = {
        user_id: currentUserId,
        name: document.getElementById('name').value,
        role: document.getElementById('role').value,
        personality: document.getElementById('personality').value,
        tone: document.getElementById('tone').value,
        likes: document.getElementById('likes').value || null,
        dislikes: document.getElementById('dislikes').value || null
    };

    try {
        const response = await fetch(`${API_BASE_URL}/api/persona`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(personaData)
        });

        if (response.ok) {
            currentPersona = await response.json();
            localStorage.setItem('persona', JSON.stringify(currentPersona));
            showChatScreen();
        } else {
            alert('Failed to create persona. Please try again.');
        }
    } catch (error) {
        console.error('Error creating persona:', error);
        alert('Network error. Please check if the server is running.');
    }
});

// Show Chat Screen
function showChatScreen() {
    setupScreen.classList.remove('active');
    chatScreen.classList.add('active');

    // Update persona info in header
    document.getElementById('personaName').textContent = currentPersona.name;
    document.getElementById('personaAvatar').textContent = currentPersona.name.charAt(0).toUpperCase();

    // Clear welcome message
    const welcomeMsg = messagesContainer.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.textContent = `Chat with ${currentPersona.name}! 💬`;
    }
}

// Load Chat History
async function loadChatHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/messages/${currentUserId}/`);
        const messages = await response.json();

        // Clear existing messages
        messagesContainer.innerHTML = '';

        if (messages.length === 0) {
            messagesContainer.innerHTML = '<div class="welcome-message"><p>Start chatting! 💬</p></div>';
            return;
        }

        // Display messages
        messages.forEach(msg => {
            addMessageToUI(msg.sender, msg.message, false);
        });

        scrollToBottom();
    } catch (error) {
        console.error('Error loading chat history:', error);
    }
}

// Chat Form Submission
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const message = messageInput.value.trim();
    if (!message) return;

    // Clear input
    messageInput.value = '';

    // Add user message to UI
    addMessageToUI('user', message);

    // Show typing indicator
    typingIndicator.style.display = 'flex';
    scrollToBottom();

    // Send message to API
    try {
        const response = await fetch(`${API_BASE_URL}/api/chat/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: currentUserId,
                message: message
            })
        });

        const data = await response.json();

        // Hide typing indicator
        typingIndicator.style.display = 'none';

        // Add AI response to UI
        addMessageToUI('ai', data.reply);
    } catch (error) {
        console.error('Error sending message:', error);
        typingIndicator.style.display = 'none';
        addMessageToUI('ai', '❌ Sorry, I encountered an error. Please make sure the server is running.');
    }
});

// Add Message to UI
function addMessageToUI(sender, text, animate = true) {
    // Remove welcome message if exists
    const welcomeMsg = messagesContainer.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.textContent = sender === 'user' ? 'You' : currentPersona.name.charAt(0).toUpperCase();

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;

    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);

    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Scroll to Bottom
function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Reset Persona
resetBtn.addEventListener('click', () => {
    if (confirm('Are you sure you want to reset your persona? This will clear all chat history.')) {
        localStorage.clear();
        location.reload();
    }
});

// Initialize app on load
initApp();
