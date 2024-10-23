import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";

document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chat-box");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");
  const playerCards = document.querySelector(".player-cards");
  const expandBtn = document.querySelector(".expand-btn");
  const evalTeamBtn = document.querySelector(".eval-team-btn");
  const refreshFunFactBtn = document.getElementById("refresh-fun-fact");
  const funFactDisplay = document.getElementById("fun-fact-display");

  const chatContainer = document.querySelector(".chat-container").parentElement; // Get parent for col-md class manipulation
  const chatColumn = chatContainer; // To handle chat column manipulation

  // Add event listener for expand functionality
  expandBtn.addEventListener("click", () => {
    playerCards.classList.toggle("expanded"); // Toggle the expanded class

    if (playerCards.classList.contains("expanded")) {
      // If expanded, adjust the grid layout
      playerCards.classList.replace("col-md-1", "col-md-5");  // Expand player cards to 8-12
  
      chatColumn.classList.replace("offset-md-4", "offset-md-2");  // Remove offset to attach chat to sidebar
    } else {
      // If collapsed, revert the grid layout
      playerCards.classList.replace("col-md-5", "col-md-1"); // Collapse player cards back to 1 column
      chatColumn.classList.replace("offset-md-2", "offset-md-4");  
    }
  });

  sendBtn.addEventListener("click", () => {
    const message = userInput.value.trim();
    sendMessage(message);
  });

  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
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

  async function fetchPlayerData(playerId) {
      try {
          const response = await fetch(`/api/player/${playerId}`); // Update this endpoint as necessary
          if (!response.ok) throw new Error("Network response was not ok");
          return await response.json(); // Assuming the response is JSON
      } catch (error) {
          console.error("Error fetching player data:", error);
          return null; // Return null if there’s an error
      }
  }

  async function sendMessage(message = null, playerList = null) {
    if (!message) {
      message = userInput.value.trim();
    }

    if (playerList) {
      message = `I build a team of ${playerList.join(', ')}. Help me evaluate and give suggestions if needed.`;
    }

    if (message) {
      appendMessage("user", message);
      userInput.value = ""; // Clear user input field

      try {
        const response = await fetch("/api/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ 
            message,
            players: playerList ? playerList : [] 
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
          updateLastBotMessage(resultData);  // Continuously update the bot's message
        }

        console.log("Stream ended");

        // Set Player names in the input fields based on response
        const teamMatch = resultData.match(/## \*Team Members\*: \*`(.+?)`\*/);
        
        if (teamMatch) {
          const playerNames = teamMatch[1].split(',').map(name => name.trim());
          
          // Loop to populate player input fields
          playerNames.forEach((name, i) => {
            if (i < 5) {
              document.getElementById(`player${i + 1}`).value = name; // Set player name to the input
  
              fetchPlayerData(name).then(player_stat => {
                player_stat = player_stat["player_stat"];
                console.log(player_stat);
                if (player_stat) {
                  // Display player info in the corresponding fields
                  document.querySelector(`#player${i + 1}-card .team-acronym`).textContent = `Team: ${player_stat['Team Acronym'] || 'N/A'}`;
                  document.querySelector(`#player${i + 1}-card .region`).textContent = `Region: ${player_stat.Region || 'N/A'}`;
                  document.querySelector(`#player${i + 1}-card .rating`).textContent = `Rating: ${player_stat['Average Rating'] || 'N/A'}`;
                  document.querySelector(`#player${i + 1}-card .ACS`).textContent = `ACS: ${player_stat['Average ACS'] || 'N/A'}`;
                  document.querySelector(`#player${i + 1}-card .ADR`).textContent = `ADR: ${player_stat['Average ADR'] || 'N/A'}`;
                  document.querySelector(`#player${i + 1}-card .KAST`).textContent = `KAST: ${player_stat['Average KAST'] || 'N/A'}`;
                  document.querySelector(`#player${i + 1}-card .agents`).textContent = `Most Played Agents: ${player_stat['Agent Names'] ? player_stat['Agent Names'].join(', ') : 'N/A'}`;
                } else {
                  console.log(`Player ${name} not found.`);
                }
              });
            }
          });
  
          // Clear remaining fields if less than 5 players
          for (let j = playerNames.length; j < 5; j++) {
            document.getElementById(`player${j + 1}`).value = ""; // Clear remaining fields
            document.querySelector(`#player${j + 1}-card .team-acronym`).textContent = `Team: `;
            document.querySelector(`#player${j + 1}-card .region`).textContent = `Region: `;
            document.querySelector(`#player${j + 1}-card .rating`).textContent = `Rating: `;
            document.querySelector(`#player${j + 1}-card .ACS`).textContent = `ACS: `;
            document.querySelector(`#player${j + 1}-card .ADR`).textContent = `ADR: `;
            document.querySelector(`#player${j + 1}-card .KAST`).textContent = `KAST: `;
            document.querySelector(`#player${j + 1}-card .agents`).textContent = `Most Played Agents: `;
          }
        }

      } catch (error) {
        console.error("Error details:", error);
        appendMessage("bot", `Error: ${error.message}`);
      }
    }
  }

  function appendMessage(sender, text) {
    const messageElem = document.createElement("div");
    messageElem.className = `message ${sender === "user" ? "user-message" : "bot-message"}`;

    if (sender === "bot") {
      const avatar = document.createElement("div");
      avatar.className = "avatar";

      const content = document.createElement("div");
      content.className = "content";
      // content.textContent = text;
      content.innerHTML = marked.parse(text) // Markdown

      messageElem.appendChild(avatar);
      messageElem.appendChild(content);
    } else {
      const content = document.createElement("div");
      content.className = "content";
      content.textContent = text;
      messageElem.appendChild(content);
    }
    chatBox.appendChild(messageElem);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function updateLastBotMessage(text) {
    const lastBotMessage = chatBox.querySelector(".bot-message:last-child .content");
    if (lastBotMessage) {
      // lastBotMessage.innerHTML = text;  
      lastBotMessage.innerHTML = marked.parse(text); // Markdown
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  }

  // Refresh fun fact button
  refreshFunFactBtn.addEventListener("click", async () => {
    try {
      const response = await fetch("/api/funfact");
      const data = await response.json();
      funFactDisplay.textContent = data.fun_fact;
    } catch (error) {
      funFactDisplay.textContent = "Error: Could not load a fun fact.";
    }
  });
});
