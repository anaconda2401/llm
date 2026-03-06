import os
import json
from config import GROQ_API_KEY, ASSISTANT_API_KEY


def initialize_storage():

    os.makedirs("storage", exist_ok=True)

    files = {
        "storage/short_memory.json": [],
        "storage/long_memory.json": [],
        "storage/settings.json": {
            "theme": "dark"
        }
    }

    for path, default in files.items():
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump(default, f, indent=2)


def validate_environment():

    missing = []

    if not GROQ_API_KEY:
        missing.append("GROQ_API_KEY")

    if not ASSISTANT_API_KEY:
        missing.append("ASSISTANT_API_KEY")

    if missing:
        raise SystemExit(f"Missing environment variables: {missing}")


def startup_checks():

    print("Running startup checks")

    validate_environment()
    initialize_storage()

    print("Startup complete")