document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chat-box");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");
  const playerCards = document.querySelector(".player-cards");
  const expandBtn = document.querySelector(".expand-btn"); // **New Code: Select the expand button**

  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  });

  // **New Code: Add event listener for expand functionality**
  expandBtn.addEventListener("click", () => {
    playerCards.classList.toggle("expanded"); // Toggle the expanded class
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
        const decoder = new TextDecoder();
        let resultData = "";
        let done = false;

        appendMessage("bot", ""); // Placeholder for streaming message

        while (!done) {
          const { done: readerDone, value } = await reader.read();
          done = readerDone;
          resultData += decoder.decode(value, { stream: !done });
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
    
    if (sender === "bot") {
      // **Bot Avatar Code**
      const avatar = document.createElement("div");
      avatar.className = "avatar";

      const content = document.createElement("div");
      content.className = "content";
      content.textContent = text;

      messageElem.appendChild(avatar);
      messageElem.appendChild(content);
    } else {
      messageElem.textContent = text;
    }
    
    chatBox.appendChild(messageElem);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function updateLastBotMessage(text) {
    const lastBotMessage = chatBox.querySelector(".bot-message:last-child .content");
    if (lastBotMessage) {
      lastBotMessage.textContent = text;
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  }
});
