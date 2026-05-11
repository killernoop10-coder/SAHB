const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const newChatBtn = document.getElementById("newChatBtn");

// CREATE MESSAGE
function createMessage(text, sender) {

    const message = document.createElement("div");
    message.className = `message ${sender}-message`;

    // USER MESSAGE
    if (sender === "user") {

        message.innerHTML = `
            <div class="message-content">
                ${text}
            </div>
        `;

    } else {

        // BOT MESSAGE
        message.innerHTML = `
            <div class="bot-header">
                <div class="bot-avatar">S</div>
                <div class="bot-name">SAHB</div>
            </div>

            <div class="message-content">
                ${text}
            </div>
        `;
    }

    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;

    return message;
}

// TYPING
function showTyping() {

    const typing = document.createElement("div");

    typing.className = "message bot-message";

    typing.id = "typing";

    typing.innerHTML = `
        <div class="bot-header">
            <div class="bot-avatar">S</div>
            <div class="bot-name">SAHB</div>
        </div>

        <div class="typing">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;

    chatBox.appendChild(typing);

    chatBox.scrollTop = chatBox.scrollHeight;
}

// REMOVE TYPING
function removeTyping() {

    const typing = document.getElementById("typing");

    if (typing) {
        typing.remove();
    }
}

// SEND MESSAGE
async function sendMessage() {

    const text = userInput.value.trim();

    if (!text) return;

    createMessage(text, "user");

    userInput.value = "";

    showTyping();

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: text
            })
        });

        const data = await response.json();

        removeTyping();

        createMessage(data.answer, "bot");

    } catch (error) {

        removeTyping();

        createMessage("Error getting response.", "bot");
    }
}

// SEND BUTTON
sendBtn.addEventListener("click", sendMessage);

// ENTER TO SEND
userInput.addEventListener("keydown", function(e){

    if(e.key === "Enter"){

        e.preventDefault();

        sendMessage();
    }
});

// NEW CHAT
newChatBtn.addEventListener("click", () => {

    chatBox.innerHTML = `
        <div class="message bot-message">

            <div class="bot-header">
                <div class="bot-avatar">S</div>
                <div class="bot-name">SAHB</div>
            </div>

            <div class="message-content">
                New conversation started 👋
            </div>

        </div>
    `;
});