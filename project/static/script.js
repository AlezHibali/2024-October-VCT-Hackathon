document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chat-box");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");
  const playerCards = document.querySelector(".player-cards");
  const expandBtn = document.querySelector(".expand-btn"); 
  const evalTeamBtn = document.querySelector(".eval-team-btn"); 

  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  });

  // Add event listener for expand functionality
  expandBtn.addEventListener("click", () => {
    playerCards.classList.toggle("expanded"); // Toggle the expanded class
  });

  // Evaluate team button
  evalTeamBtn.addEventListener("click", () => {
    const player1 = document.getElementById('player1').value || null;
    const player2 = document.getElementById('player2').value || null;
    const player3 = document.getElementById('player3').value || null;
    const player4 = document.getElementById('player4').value || null;
    const player5 = document.getElementById('player5').value || null;

    // Send the message with the player list
    const playerList = [player1, player2, player3, player4, player5];
    sendMessage(null, playerList);
  });

  async function sendMessage(message = null, playerList = null) {
    // If no message is passed, use the user input
    if (!message) {
      message = userInput.value.trim();
    }

    // Check if a player list is provided
    if (playerList) {
      message = `I build a team of ${playerList.join(', ')}. Help me evaluate and give suggestions if needed.`;
    }

    if (message) {
      appendMessage("user", message);
      userInput.value = ""; // Clear user input field if it's a user message

      try {
        const response = await fetch("/api/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ 
            message,
            players: playerList ? playerList : [] // Sending the player list data if available
          }),
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
          updateLastBotMessage(resultData);  // Continuously update the bot's message as it streams in
        }

        console.log("Stream ended");

        // Set Player names in the input fields based on response
        const playerNames = resultData.match(/<(.*?)>/g);
        if (playerNames) {
          playerNames.forEach((name, i) => {
            document.getElementById(`player${i + 1}`).value = name.replace(/<|>/g, '').trim();
          });
        }

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
