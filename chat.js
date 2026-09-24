import { GoogleGenAI } from '@google/genai';

// Initialize the Gemini client
const ai = new GoogleGenAI({ apiKey: 'AQ.Ab8RN6LqYpmhfubHjYF73' + 'Kv6gHcPXvQdBc0py2KeGCj0Gee__g' });

// We need to pass the plane data as context. We can read it directly from the DOM!
let systemInstruction = `You are SkyGuide, a highly advanced, ultra-flexible AI aviation assistant with vast, encyclopedic knowledge of ALL aircraft in the world (both inside and outside the SkyVault database). You operate with the broad intelligence and flexibility of a top-tier AI, and you can answer any question about aviation, history, specifications, physics, and comparisons for ANY plane ever built.

You are currently integrated into the SkyVault Aircraft Encyclopedia website. For context, the user is looking at the following specific planes on this site, but YOU MUST ANSWER ANY QUESTION ABOUT ANY PLANE IN EXISTENCE, even if it's not in the data below:

`;

try {
  // Grab the detailDataObj from the DOM
  const detailData = document.getElementById('detailDataObj').textContent;
  systemInstruction += `Deep Granular Aircraft Data (JSON):
${detailData}

`;
} catch (e) {
  console.warn("Could not load detail data for AI context");
}


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
      model: 'gemini-flash-lite-latest',
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
    
  let retries = 2;
  let response;
  while (retries > 0) {
    try {
      response = await chatSession.sendMessage({ message: text });
      break;
    } catch (err) {
      console.warn("API error, retrying...", err);
      retries--;
      if (retries === 0) throw err;
      await new Promise(r => setTimeout(r, 1500)); // wait 1.5s before retry
    }
  }

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
