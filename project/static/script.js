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

  async function sendMessage() {
    const message = userInput.value.trim();
    if (message) {
      appendMessage("user", message);
      userInput.value = "";

      try {
        const response = await fetch("/api/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message }),
        });

        if (!response.body) {
          throw new Error("ReadableStream not supported.");
        }

        const reader = response.body.getReader();
        let decoder = new TextDecoder();
        let resultData = "";
        let done = false;

        appendMessage("bot", ""); // Placeholder for streaming message

        while (!done) {
          const { done: readerDone, value } = await reader.read();
          done = readerDone;
          resultData += decoder.decode(value, { stream: !done });
          console.log(resultData);
          // Update the last bot message with the current stream content
          updateLastBotMessage(resultData);
        }

        console.log("Stream ended");

      } catch (error) {
        appendMessage("bot", "Error: Could not connect to server.");
      }
    }
  }

  function appendMessage(sender, text) {
    const messageElem = document.createElement("div");
    messageElem.className = `message ${sender === "user" ? "user-message" : "bot-message"}`;
    messageElem.textContent = text;
    chatBox.appendChild(messageElem);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function updateLastBotMessage(text) {
    const lastBotMessage = chatBox.querySelector(".bot-message:last-child");
    if (lastBotMessage) {
      lastBotMessage.textContent = text;
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  }
});
