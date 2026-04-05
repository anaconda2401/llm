from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import jwt
import threading
import json

from config import AUTH_VAULT_PUBLIC_KEY, PUBLIC_API_KEY, SHARE_PUBLIC_MEMORY
from memory.short_memory import add_message, get_memory, clear_short_memory
from memory.long_memory import add_long_memory, get_long_memory, clear_long_memory
from llm import generate, extract_long_term_memory

SETTINGS_FILE = "storage/settings.json"

app = Flask(__name__)
CORS(app)

SYSTEM_PROMPT = {
    "role": "system",
    "content": """
You are Ella — a natural voice-friendly assistant.

Speak clearly and briefly like a real person.

Core Style Rules:
- 2–3 short sentences by default
- Under 80 words
- No over-explaining
- No article style answers
- Do not repeat the user's question

Response Discipline:
- Only answer what was asked
- No jokes unless asked
- No extra commentary
- Do not say things like "I already knew that"

Behavior:
- Ask one short clarifying question if needed
- Stay natural and conversational

Memory Usage:
You may receive long-term memory about the user.
Treat those as facts and use them when relevant.
"""
}

def verify_token(req):
    """Secures the endpoint by validating the Auth Vault RS256 JWT."""
    auth_header = req.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return False
        
    token = auth_header.split(" ")[1]
    
    try:
        # Decodes using your Auth Vault Public Key and RS256 algorithm
        jwt.decode(token, AUTH_VAULT_PUBLIC_KEY, algorithms=["RS256"])
        return True
    except Exception as e:
        print(f"Token validation failed: {e}")
        return False

@app.route("/")
def home():
    return "Ella Assistant Backend Running"

@app.route("/chat", methods=["POST"])
def chat():
    if not verify_token(request):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "Message required"}), 400

    add_message("user", user_input)

    # Background thread for memory extraction to prevent UI lag
    def process_memory(msg):
        fact = extract_long_term_memory(msg)
        if fact:
            add_long_memory(fact)

    threading.Thread(target=process_memory, args=(user_input,)).start()

    short_memory = get_memory()
    long_memory = get_long_memory()

    memory_text = "\n".join(long_memory)

    messages = [
        SYSTEM_PROMPT,
        {
            "role": "system",
            "content": f"""
Long-term memory about the user:

{memory_text}

Use this information when relevant.
"""
        }
    ] + short_memory

    response = generate(messages)
    add_message("assistant", response)

    return jsonify({"response": response})

@app.route("/memory", methods=["GET"])
def view_memory():
    if not verify_token(request):
        return jsonify({"error": "Unauthorized"}), 401

    short_memory = get_memory()
    long_memory = get_long_memory()

    return jsonify({
        "short_memory": short_memory,
        "long_memory": long_memory
    })

@app.route("/memory/clear", methods=["POST"])
def clear_memory():
    if not verify_token(request):
        return jsonify({"error": "Unauthorized"}), 401

    clear_short_memory()
    clear_long_memory()

    return jsonify({"status": "Memory cleared"})

@app.route("/settings", methods=["GET"])
def get_settings():
    with open(SETTINGS_FILE) as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/settings", methods=["POST"])
def update_settings():
    data = request.json
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return jsonify({"status": "updated"})

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

def verify_public_api_key(req):
    """Secures the endpoint for curl and external scripts."""
    key = req.headers.get("X-API-KEY")
    return key == PUBLIC_API_KEY and PUBLIC_API_KEY is not None

@app.route("/api/chat", methods=["POST"])
def public_chat():
    """Stateless OR Stateful endpoint for programmatic access, based on config."""
    if not verify_public_api_key(request):
        return jsonify({"error": "Invalid or missing API Key"}), 401

    data = request.json
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "Message required"}), 400

    if SHARE_PUBLIC_MEMORY:
        # --- STATEFUL MODE (Shares memory with Dashboard) ---
        add_message("user", user_input)

        def process_memory(msg):
            fact = extract_long_term_memory(msg)
            if fact:
                add_long_memory(fact)

        threading.Thread(target=process_memory, args=(user_input,)).start()

        short_memory = get_memory()
        long_memory = get_long_memory()
        memory_text = "\n".join(long_memory)

        messages = [
            SYSTEM_PROMPT,
            {
                "role": "system",
                "content": f"Long-term memory about the user:\n\n{memory_text}\n\nUse this information when relevant."
            }
        ] + short_memory

        response = generate(messages)
        add_message("assistant", response)

    else:
        # --- STATELESS MODE (Clean slate, no memory writing) ---
        messages = [
            SYSTEM_PROMPT,
            {"role": "user", "content": user_input}
        ]
        response = generate(messages)

    return jsonify({
        "response": response
    })


if __name__ == "__main__":
    app.run(debug=True) # Turn back to False when deploying