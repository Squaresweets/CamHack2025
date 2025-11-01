from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)
latest_char = None

def generate_reply(message: str) -> str:
    """Very small, deterministic-ish reply generator for the demo.
    This is intentionally lightweight and doesn't depend on external services.
    """
    msg = (message or "").strip().lower()
    if not msg:
        return "Say something — I'm listening."

    # quick rule-based responses
    if any(word in msg for word in ["hi", "hello", "hey"]):
        return random.choice(["Hi there!", "Hello — how can I help?", "Hey! What's up?"])
    if "help" in msg:
        return "Tell me anything and I'll echo back with a friendly reply. Try asking a question."
    if msg.endswith("?"):
        return random.choice(["That's a great question.", "I don't know for sure, but I can try to help.", "Hmmm — what do you think?"])
    if any(word in msg for word in ["thanks", "thank you"]):
        return "You're welcome — glad to help!"

    # small transformations for variety
    if len(msg.split()) == 1:
        return f"You said: {msg}. Tell me more."

    return f"Echo: {message}"



@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    message = data.get("message", "")
    latest_message = message
    reply = generate_reply(message)
    return jsonify({"reply": reply})

@app.route('/check_for_updates', methods=['GET'])
def check_for_updates():
    """Frontend polls this route every few seconds."""

    global latest_char, last_updated
    if latest_char:
        data = latest_char
        latest_char = None  # clear after sending (optional)
        return jsonify(new_data=True, chars=data)
    return jsonify(new_data=False)

@app.route('/check_new_message', methods=['GET'])
def check_new_message():
    global latest_message
    if latest_message:
        data = latest_message
        latest_message = None  # clear after sending (optional)
        return jsonify(new_data=True, message=data)
    return jsonify(new_data=False)


@app.route('/newchar/<char>', methods=['GET'])
def newchar(char):
    """Endpoint for injecting a new character from external tools."""
    global latest_char
    if char:
        if latest_char is None:
            latest_char = ""
        latest_char += char
        return jsonify(success=True)
    return jsonify(success=False), 400


if __name__ == "__main__":
    # Bind to localhost on port 5000
    app.run(host="127.0.0.1", port=5000)
