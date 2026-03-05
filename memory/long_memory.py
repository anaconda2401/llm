import json
import os

LONG_MEMORY_FILE = "storage/long_memory.json"


def load_long_memory():

    if not os.path.exists(LONG_MEMORY_FILE):
        return []

    with open(LONG_MEMORY_FILE, "r") as f:
        return json.load(f)


def save_long_memory(memory):

    os.makedirs("storage", exist_ok=True)

    with open(LONG_MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def add_long_memory(fact):

    if not fact:
        return

    memory = load_long_memory()

    normalized = [m.lower() for m in memory]

    if fact.lower() not in normalized:
        memory.append(fact)

    save_long_memory(memory)


def get_long_memory():
    return load_long_memory()

def clear_long_memory():
    save_long_memory([])