import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PUBLIC_API_KEY = os.getenv("PUBLIC_API_KEY")
AUTH_VAULT_PUBLIC_KEY = os.getenv("AUTH_VAULT_PUBLIC_KEY", "").replace('\\n', '\n')

# Toggle: Controls whether the public API shares memory with the dashboard False or true
SHARE_PUBLIC_MEMORY = os.getenv("SHARE_PUBLIC_MEMORY", "true").lower() in ('true', '1', 't')

MODEL_NAME = "llama-3.1-8b-instant"
SHORT_MEMORY_LIMIT = 50