const chatMessages = document.getElementById("chatMessages");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const clearButton = document.getElementById("clearButton");


function addMessage(role, content) {
    const welcome = chatMessages.querySelector(".welcome");

    if (welcome) {
        welcome.remove();
    }

    const article = document.createElement("article");
    article.className = `message ${role}`;

    const label = document.createElement("span");
    label.className = "message-label";
    label.textContent = role === "user" ? "You" : "Assistant";

    const body = document.createElement("div");

    // Treat messages as plain text, not executable HTML.
    body.textContent = content;

    article.append(label, body);
    chatMessages.appendChild(article);

    chatMessages.scrollTop = chatMessages.scrollHeight;

    return article;
}


async function loadHistory() {
    try {
        const response = await fetch("/api/history");

        if (!response.ok) {
            throw new Error("Could not load chat history");
        }

        const data = await response.json();

        if (data.messages && data.messages.length > 0) {
            chatMessages.innerHTML = "";

            data.messages.forEach((message) => {
                addMessage(message.role, message.content);
            });
        }
    } catch (error) {
        console.error(error);
    }
}


chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    addMessage("user", message);
    messageInput.value = "";

    sendButton.disabled = true;

    const pending = addMessage("assistant", "Thinking...");

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        pending.remove();

        if (!response.ok) {
            throw new Error(data.error || "Request failed");
        }

        addMessage("assistant", data.reply);

    } catch (error) {
        pending.remove();

        addMessage(
            "assistant",
            "Unable to get a response. Check the server and try again."
        );

        console.error(error);

    } finally {
        sendButton.disabled = false;
        messageInput.focus();
    }
});


clearButton.addEventListener("click", async () => {
    const confirmed = confirm("Delete all saved chat messages?");

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch("/api/clear", {
            method: "POST"
        });

        if (!response.ok) {
            throw new Error("Could not clear history");
        }

        chatMessages.innerHTML = "";

        const welcome = document.createElement("div");
        welcome.className = "welcome";

        const heading = document.createElement("h2");
        heading.textContent = "Chat cleared";

        const paragraph = document.createElement("p");
        paragraph.textContent = "Start a new conversation below.";

        welcome.append(heading, paragraph);
        chatMessages.appendChild(welcome);

    } catch (error) {
        alert("Could not clear the chat. Please try again.");
    }
});


document.querySelectorAll(".suggestion").forEach((button) => {
    button.addEventListener("click", () => {
        messageInput.value = button.dataset.prompt || "";
        messageInput.focus();
    });
});


messageInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        chatForm.requestSubmit();
    }
});


loadHistory();