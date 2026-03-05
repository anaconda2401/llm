import json
import os
from config import SHORT_MEMORY_LIMIT

MEMORY_FILE = "storage/short_memory.json"


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(memory):

    os.makedirs("storage", exist_ok=True)

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def add_message(role, content):

    memory = load_memory()

    memory.append({
        "role": role,
        "content": content
    })

    memory = memory[-SHORT_MEMORY_LIMIT:]

    save_memory(memory)


def get_memory():
    return load_memory()


def clear_short_memory():
    save_memory([])