const chat = document.getElementById("chat");
const input = document.getElementById("input");
const send = document.getElementById("send");
const resetBtn = document.getElementById("reset-btn");
const debugToggle = document.getElementById("debug-toggle");

const themeToggle = document.getElementById("theme-toggle");

const savedTheme = localStorage.getItem("theme") || "dark";
document.documentElement.setAttribute("data-theme", savedTheme);
themeToggle.textContent = savedTheme === "light" ? "◐" : "◑";

themeToggle.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
    themeToggle.textContent = next === "light" ? "◐" : "◑";
});

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function renderMarkdown(text) {
    return escapeHtml(text)
        .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
        .replace(/_(.+?)_/g, "<em>$1</em>")
        .replace(/•/g, "›")
        .replace(/\n/g, "<br>");
}

function addMessage(role, text, debug) {
    const div = document.createElement("div");
    div.className = "message " + role;

    const label = document.createElement("div");
    label.className = "msg-label";
    label.textContent = role === "user" ? "you" : "cinebot";
    div.appendChild(label);

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerHTML = renderMarkdown(text);
    div.appendChild(bubble);

    if (debug && role === "bot" && debugToggle.checked) {
        const dbg = document.createElement("div");
        dbg.className = "debug";
        dbg.textContent = `intent: ${debug.intent || "?"} (${debug.confidence}) › entities: ${JSON.stringify(debug.entities)}`;
        div.appendChild(dbg);
    }

    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function showTyping() {
    const wrap = document.createElement("div");
    wrap.className = "message bot";
    wrap.id = "typing-indicator";
    const label = document.createElement("div");
    label.className = "msg-label";
    label.textContent = "cinebot";
    wrap.appendChild(label);
    const dots = document.createElement("div");
    dots.className = "typing-dots";
    dots.innerHTML = "<span></span><span></span><span></span>";
    wrap.appendChild(dots);
    chat.appendChild(wrap);
    chat.scrollTop = chat.scrollHeight;
}

function hideTyping() {
    const el = document.getElementById("typing-indicator");
    if (el) el.remove();
}

async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    addMessage("user", text);
    input.value = "";
    send.disabled = true;
    showTyping();

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        hideTyping();
        addMessage("bot", data.reply, data.debug);
    } catch (e) {
        hideTyping();
        addMessage("bot", "⚠ Error connecting to server.");
    } finally {
        send.disabled = false;
        input.focus();
    }
}

send.addEventListener("click", sendMessage);
input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});

resetBtn.addEventListener("click", async () => {
    await fetch("/reset", { method: "POST" });
    chat.innerHTML = "";
    addMessage("bot", "Conversation reset. Hi, I'm CineBot — what movie can I help you with?");
});

addMessage("bot", "Hi there! I'm **CineBot** — your AI movie companion.\n\nTry asking me:\n› _Recommend me a sci-fi movie_\n› _Tell me about Inception_\n› _What movies has Tom Hanks been in?_\n› _Show me Nolan movies_");