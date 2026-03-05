from memory import add_message, get_memory
from llm import generate

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are a helpful AI assistant."
}

print("LLM Assistant Ready (type 'exit' to stop)\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    add_message("user", user_input)

    history = get_memory()

    messages = [SYSTEM_PROMPT] + history

    response = generate(messages)

    print("\nAssistant:", response, "\n")

    add_message("assistant", response)