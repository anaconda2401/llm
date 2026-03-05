from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME

client = Groq(api_key=GROQ_API_KEY)


def generate(messages):

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.7
    )

    return completion.choices[0].message.content.strip()


def extract_long_term_memory(user_message):

    messages = [
        {
            "role": "system",
            "content": """
Extract important long-term facts from the message.

Only extract:
- name
- interests
- preferences
- profession
- projects
- goals

Return ONE short sentence.

Examples:

User: My name is John
Output: User's name is John

User: I like Python
Output: User likes Python

If nothing important exists return EXACTLY:
NONE
"""
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    result = generate(messages).strip()

    if result.upper() == "NONE":
        return None

    blacklist = [
        "no important",
        "i don't have",
        "no information",
        "not mentioned",
        "none,"
    ]

    for word in blacklist:
        if word in result.lower():
            return None

    if len(result.split()) > 20:
        return None

    return result