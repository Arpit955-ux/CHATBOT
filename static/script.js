const heroCard = document.getElementById("hero-card");
const chatCard = document.getElementById("chat-card");
const startBtn = document.getElementById("start-btn");
const chatWindow = document.getElementById("chat-window");
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");

function addMessage(text, type) {
  const el = document.createElement("div");
  el.className = type === "user" ? "user-message" : "bot-message";
  el.textContent = text;
  chatWindow.appendChild(el);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage(message) {
  addMessage(message, "user");

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error("Request failed");
    }

    const data = await response.json();
    const replies = Array.isArray(data.replies) ? data.replies : [];

    if (replies.length === 0) {
      addMessage("I did not receive any response. Please try again.", "bot");
      return;
    }

    replies.forEach((reply) => addMessage(reply, "bot"));
  } catch (error) {
    addMessage("Unable to connect to the chatbot server. Please try again.", "bot");
  }
}

startBtn.addEventListener("click", () => {
  heroCard.classList.add("hidden");
  chatCard.classList.remove("hidden");
  messageInput.focus();
});

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = messageInput.value.trim();

  if (!message) {
    return;
  }

  messageInput.value = "";
  await sendMessage(message);
  messageInput.focus();
});
