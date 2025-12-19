// API Configuration
const API_BASE = '/api';
let currentUser = null;

// DOM Elements
const setupScreen = document.getElementById('setupScreen');
const chatScreen = document.getElementById('chatScreen');
const personaForm = document.getElementById('personaForm');
const chatForm = document.getElementById('chatForm');
const messagesContainer = document.getElementById('messagesContainer');
const messageInput = document.getElementById('messageInput');
const typingIndicator = document.getElementById('typingIndicator');
const personaName = document.getElementById('personaName');
const personaAvatar = document.getElementById('personaAvatar');
const resetBtn = document.getElementById('resetBtn');
const resetModal = document.getElementById('resetModal');
const cancelReset = document.getElementById('cancelReset');
const confirmReset = document.getElementById('confirmReset');

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    checkExistingUser();
    setupEventListeners();
});

function setupEventListeners() {
    personaForm.addEventListener('submit', handlePersonaSubmit);
    chatForm.addEventListener('submit', handleChatSubmit);
    resetBtn.addEventListener('click', showResetModal);
    cancelReset.addEventListener('click', hideResetModal);
    confirmReset.addEventListener('click', handleReset);

    // Close modal when clicking outside
    resetModal.addEventListener('click', (e) => {
        if (e.target === resetModal) {
            hideResetModal();
        }
    });
}

// Check for existing user in localStorage
function checkExistingUser() {
    const userId = localStorage.getItem('userId');
    if (userId) {
        currentUser = { id: parseInt(userId) };
        loadPersona();
    }
}

// Create new user
async function createUser() {
    try {
        const response = await fetch(`${API_BASE}/users/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await response.json();
        currentUser = data;
        localStorage.setItem('userId', data.id);
        return data;
    } catch (error) {
        console.error('Error creating user:', error);
        alert('Failed to create user. Please try again.');
    }
}

// Handle Persona Form Submit
async function handlePersonaSubmit(e) {
    e.preventDefault();

    if (!currentUser) {
        await createUser();
    }

    // Collect selected personality traits
    const personalityCheckboxes = document.querySelectorAll('input[name="personality"]:checked');
    const personality = Array.from(personalityCheckboxes).map(cb => cb.value).join(', ');

    // Collect selected likes
    const likesCheckboxes = document.querySelectorAll('input[name="likes"]:checked');
    const likes = Array.from(likesCheckboxes).map(cb => cb.value).join(', ');

    // Collect selected dislikes
    const dislikesCheckboxes = document.querySelectorAll('input[name="dislikes"]:checked');
    const dislikes = Array.from(dislikesCheckboxes).map(cb => cb.value).join(', ');

    // Validate at least one personality trait is selected
    if (!personality) {
        alert('Please select at least one personality trait');
        return;
    }

    const personaData = {
        user_id: currentUser.id,
        name: document.getElementById('name').value,
        role: document.getElementById('role').value,
        personality: personality,
        tone: document.getElementById('tone').value,
        likes: likes || '',
        dislikes: dislikes || ''
    };

    try {
        const response = await fetch(`${API_BASE}/personas/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(personaData)
        });

        if (response.ok) {
            const persona = await response.json();
            showChatScreen(persona);
            loadChatHistory();
        } else {
            alert('Failed to create persona. Please try again.');
        }
    } catch (error) {
        console.error('Error creating persona:', error);
        alert('Failed to create persona. Please try again.');
    }
}

// Load existing persona
async function loadPersona() {
    try {
        const response = await fetch(`${API_BASE}/personas/${currentUser.id}/`);
        if (response.ok) {
            const persona = await response.json();
            showChatScreen(persona);
            loadChatHistory();
        }
    } catch (error) {
        console.error('Error loading persona:', error);
    }
}

// Show chat screen
function showChatScreen(persona) {
    setupScreen.classList.remove('active');
    chatScreen.classList.add('active');

    personaName.textContent = persona.name;
    personaAvatar.textContent = persona.name.charAt(0).toUpperCase();
}

// Load chat history
async function loadChatHistory() {
    try {
        const response = await fetch(`${API_BASE}/messages/${currentUser.id}/`);
        if (response.ok) {
            const messages = await response.json();
            messagesContainer.innerHTML = '';
            messages.forEach(msg => displayMessage(msg.message, msg.sender));
        }
    } catch (error) {
        console.error('Error loading chat history:', error);
    }
}

// Handle Chat Submit
async function handleChatSubmit(e) {
    e.preventDefault();

    const message = messageInput.value.trim();
    if (!message) return;

    // Display user message
    displayMessage(message, 'user');
    messageInput.value = '';

    // Show typing indicator
    typingIndicator.classList.add('active');

    try {
        const response = await fetch(`${API_BASE}/chat/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: currentUser.id,
                message: message
            })
        });

        if (response.ok) {
            const data = await response.json();
            typingIndicator.classList.remove('active');
            displayMessage(data.reply, 'ai');
        } else {
            typingIndicator.classList.remove('active');
            displayMessage('Sorry, I had trouble responding. Please try again.', 'ai');
        }
    } catch (error) {
        console.error('Error sending message:', error);
        typingIndicator.classList.remove('active');
        displayMessage('Sorry, I had trouble responding. Please try again.', 'ai');
    }
}

// Display message in chat
function displayMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = text;

    messageDiv.appendChild(bubble);
    messagesContainer.appendChild(messageDiv);

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Show Reset Modal
function showResetModal() {
    resetModal.classList.add('active');
}

// Hide Reset Modal
function hideResetModal() {
    resetModal.classList.remove('active');
}

// Handle Reset
function handleReset() {
    localStorage.removeItem('userId');
    currentUser = null;
    chatScreen.classList.remove('active');
    setupScreen.classList.add('active');
    personaForm.reset();
    messagesContainer.innerHTML = '<div class="welcome-message"><p>👋 Start chatting with your AI companion!</p></div>';
    hideResetModal();
}
