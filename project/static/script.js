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

        fetch("/api/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ message })
        })
        .then(response => response.json())
        .then(data => {
          appendMessage("bot", data.bot_message);
        })
        .catch(error => {
          appendMessage("bot", "Error: Could not connect to server.");
        });
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
