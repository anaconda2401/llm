import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Grab the public key instead of a secret string
AUTH_VAULT_PUBLIC_KEY = os.getenv("AUTH_VAULT_PUBLIC_KEY").replace('\\n', '\n')

MODEL_NAME = "llama-3.1-8b-instant"
SHORT_MEMORY_LIMIT = 50

PUBLIC_API_KEY = os.getenv("PUBLIC_API_KEY")