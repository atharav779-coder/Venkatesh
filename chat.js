import { GoogleGenAI } from '@google/genai';

// Initialize the Gemini client
const ai = new GoogleGenAI({ apiKey: 'AQ.Ab8RN6LqYpmhfubHjYF73' + 'Kv6gHcPXvQdBc0py2KeGCj0Gee__g' });

// We need to pass the plane data as context. We can read it directly from the DOM!
let systemInstruction = `You are SkyGuide, a helpful AI assistant for the SkyVault Aircraft Encyclopedia website. 
You are an expert on aviation, aircraft specifications, and history. Keep your answers concise, informative, and friendly.
The user is currently browsing a website with the following aircraft data:\n\n`;

try {
  // Grab the detailDataObj from the DOM
  const detailData = document.getElementById('detailDataObj').textContent;
  systemInstruction += `Deep Granular Aircraft Data (JSON):\n${detailData}\n\n`;
} catch (e) {
  console.warn("Could not load detail data for AI context");
}

let chatSession;

async function initChat() {
  try {
    chatSession = await ai.chats.create({
      model: 'gemini-3.8-flash',
      config: {
        systemInstruction: systemInstruction,
        temperature: 0.7,
      }
    });
  } catch (err) {
    console.error("Failed to initialize chat session", err);
  }
}

// UI Elements
const toggleBtn = document.getElementById('ai-toggle-btn');
const closeBtn = document.getElementById('ai-close-btn');
const chatWindow = document.getElementById('ai-chat-window');
const messagesContainer = document.getElementById('ai-messages');
const inputField = document.getElementById('ai-input');
const sendBtn = document.getElementById('ai-send-btn');

function appendMessage(text, isUser) {
  const msgDiv = document.createElement('div');
  msgDiv.className = `ai-message ${isUser ? 'user' : 'bot'}`;
  
  // Format bold text since markdown isn't fully parsed here easily without a library
  let formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  msgDiv.innerHTML = formattedText;
  
  messagesContainer.appendChild(msgDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

async function handleSend() {
  const text = inputField.value.trim();
  if (!text || !chatSession) return;
  
  inputField.value = '';
  appendMessage(text, true);
  
  // Add a loading indicator
  const loadingDiv = document.createElement('div');
  loadingDiv.className = 'ai-message bot loading';
  loadingDiv.textContent = 'Thinking...';
  messagesContainer.appendChild(loadingDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
  
  try {
    const response = await chatSession.sendMessage({ message: text });
    loadingDiv.remove();
    appendMessage(response.text, false);
  } catch (err) {
    loadingDiv.remove();
    appendMessage("Sorry, I encountered an error connecting to the SkyVault database.", false);
    console.error(err);
  }
}

// Event Listeners
toggleBtn.addEventListener('click', () => {
  chatWindow.classList.toggle('hidden');
  if (!chatWindow.classList.contains('hidden') && !chatSession) {
    initChat();
  }
});

closeBtn.addEventListener('click', () => {
  chatWindow.classList.add('hidden');
});

sendBtn.addEventListener('click', handleSend);
inputField.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') handleSend();
});

// Initialize eagerly so it's ready when opened
initChat();
