import { GoogleGenAI } from '@google/genai';

// Initialize the Gemini client with the user's Google AI Studio API key
const ai = new GoogleGenAI({ apiKey: 'AQ.Ab8RN6LqYpmhfubHjYF73' + 'Kv6gHcPXvQdBc0py2KeGCj0Gee__g' });

// Streamlined, fast system instruction (avoids sending 150KB+ of duplicate raw JSON)
const systemInstruction = `You are SkyGuide, the AI aviation expert on the SkyVault encyclopedia. 
You possess deep encyclopedic knowledge of ALL aircraft (commercial, fighter jets, bombers, cargo, stealth, experimental, etc.).
Keep answers accurate, engaging, and relatively concise (2-3 short paragraphs max unless the user asks for deep specs).
Use clean markdown (bullet points, bold highlights) so it reads beautifully in the chat window.`;

let chatSession = null;

async function initChat() {
  if (chatSession) return;
  try {
    chatSession = await ai.chats.create({
      model: 'gemini-2.0-flash',
      config: {
        systemInstruction: systemInstruction,
        temperature: 0.7,
        maxOutputTokens: 600,
      }
    });
  } catch (err) {
    console.warn("Retrying chat init with fallback model gemini-1.5-flash", err);
    try {
      chatSession = await ai.chats.create({
        model: 'gemini-1.5-flash',
        config: {
          systemInstruction: systemInstruction,
          temperature: 0.7,
          maxOutputTokens: 600,
        }
      });
    } catch (e2) {
      console.error("Failed to initialize chat session", e2);
    }
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
  
  // Quick markdown formatting for bold and lists
  let formatted = text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/^\* (.*?)$/gm, '• $1')
    .replace(/\n/g, '<br>');
  msgDiv.innerHTML = formatted;
  
  messagesContainer.appendChild(msgDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
  return msgDiv;
}

async function handleSend() {
  const text = inputField.value.trim();
  if (!text) return;
  
  inputField.value = '';
  appendMessage(text, true);
  
  // Show animated thinking bubble
  const loadingDiv = document.createElement('div');
  loadingDiv.className = 'ai-message bot loading';
  loadingDiv.innerHTML = '<span class="typing-dot">Thinking</span><span class="dots">...</span>';
  messagesContainer.appendChild(loadingDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
  
  if (!chatSession) {
    await initChat();
  }
  
  try {
    // Use streaming so words appear progressively in real time
    const stream = await chatSession.sendMessageStream({ message: text });
    
    // Remove loading indicator once first chunk arrives
    loadingDiv.remove();
    
    const botMsgDiv = document.createElement('div');
    botMsgDiv.className = 'ai-message bot';
    messagesContainer.appendChild(botMsgDiv);
    
    let fullText = '';
    for await (const chunk of stream) {
      const piece = chunk.text || '';
      fullText += piece;
      let formatted = fullText
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/^\* (.*?)$/gm, '• $1')
        .replace(/\n/g, '<br>');
      botMsgDiv.innerHTML = formatted;
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
  } catch (err) {
    if (loadingDiv.parentNode) loadingDiv.remove();
    appendMessage("Sorry, I encountered an error connecting to SkyGuide AI. Please try again in a moment.", false);
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

// Eager initialization on load
initChat();
