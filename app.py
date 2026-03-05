from flask import Flask, request, jsonify

from config import ASSISTANT_API_KEY
from memory.short_memory import add_message, get_memory
from memory.long_memory import add_long_memory, get_long_memory

from memory.short_memory import clear_short_memory
from memory.long_memory import clear_long_memory

from llm import generate, extract_long_term_memory

app = Flask(__name__)


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


def verify_api_key(req):

    key = req.headers.get("X-API-KEY")

    if key != ASSISTANT_API_KEY:
        return False

    return True


@app.route("/")
def home():
    return "Ella Assistant Backend Running"


@app.route("/chat", methods=["POST"])
def chat():

    if not verify_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "Message required"}), 400

    add_message("user", user_input)

    fact = extract_long_term_memory(user_input)

    if fact:
        add_long_memory(fact)

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

    return jsonify({
        "response": response
    })

@app.route("/memory", methods=["GET"])
def view_memory():

    if not verify_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    short_memory = get_memory()
    long_memory = get_long_memory()

    return jsonify({
        "short_memory": short_memory,
        "long_memory": long_memory
    })

@app.route("/memory/clear", methods=["POST"])
def clear_memory():

    if not verify_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    clear_short_memory()
    clear_long_memory()

    return jsonify({
        "status": "Memory cleared"
    })


if __name__ == "__main__":
    app.run(debug=False)