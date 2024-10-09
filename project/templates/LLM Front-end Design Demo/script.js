document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
  
    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        sendMessage();
      }
    });
  
    function sendMessage() {
      const message = userInput.value.trim();
      if (message) {
        appendMessage("user", message);
        userInput.value = "";
        setTimeout(() => appendMessage("bot", "Processing..."), 500);
        // Simulate API call or response
        setTimeout(() => appendMessage("bot", "This is a response from the bot."), 1500);
      }
    }
  
    function appendMessage(sender, text) {
      const messageElem = document.createElement("div");
      messageElem.className = `message ${sender === "user" ? "user-message" : "bot-message"}`;
      messageElem.textContent = text;
      chatBox.appendChild(messageElem);
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  });
  