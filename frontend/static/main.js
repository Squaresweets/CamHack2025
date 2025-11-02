const messagesEl = document.getElementById("messages");
const form = document.getElementById("composer");
const input = document.getElementById("input");
let currentId = 0;

function appendMessage(text, who, id) {
  const wrapper = document.createElement("div");
  wrapper.className = "msg " + who;
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.id = id;
  bubble.textContent = text;
  wrapper.appendChild(bubble);
  messagesEl.appendChild(wrapper);
  messagesEl.scrollTo({ top: messagesEl.scrollHeight, behavior: "smooth" });
}

function appendCharacter(id, newText) {
  const bubble = document.getElementById(id);
  if (bubble) {
    bubble.textContent = bubble.textContent + newText;
  }
}

async function sendMessage(text) {
  appendMessage(text, "user");
  input.value = "";
  input.disabled = true;
  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
  } catch (err) {
    appendMessage("Server error. Is the backend running?", "bot");
    console.error(err);
  } finally {
    input.disabled = false;
    input.focus();
  }
}

setInterval(async () => {
  const res = await fetch("/check_for_updates");
  const data = await res.json();
  console.log("Checked for updates:", data);
  if (data.new_data) {
    for (let char of data.chars) {
      if (char == "]") {
        console.log("New message detected");
        appendMessage("", "bot", ++currentId);
      } else {
        if (currentId === 0) {
          appendMessage(char, "bot", ++currentId);
        } else {
          appendCharacter(currentId, char);
        }
      }
    }
  }
}, 500);

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const txt = input.value.trim();
  if (!txt) return;
  sendMessage(txt);
});

input.focus();
