# 🤖 Ella Assistant Backend

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Framework-Flask-black?logo=flask)
![Groq](https://img.shields.io/badge/LLM-Groq_API-f5652e)
![License](https://img.shields.io/badge/License-Personal_Use-green)

A lightweight, intelligent AI assistant backend built with **Flask** and the **Groq LLM API**. 

Ella features a dedicated persona, short-term conversational context, and dynamic long-term memory extraction to provide a deeply personalized chat experience. It is designed to be highly portable and easily deployable on lightweight hosting environments like PythonAnywhere.

---

## ✨ Features

* **⚡ Groq LLM Integration:** Blazing fast inference using Groq's API.
* **🧠 Dual Memory System:**
    * *Short-term:* Retains the last 50 messages for immediate conversational context.
    * *Long-term:* Dynamically extracts and stores persistent user facts (e.g., "User's name is Aswin", "User likes Python").
* **🔒 Secure:** API key authentication for all endpoints and local `.env` secret management.
* **🪶 Lightweight:** Minimal dependencies (<10MB), perfect for small VPS or containerized deployments.
* **🛠️ Debug Ready:** Built-in endpoints to inspect and manage memory states.

---

## 🏗️ Architecture & Memory Flow

```text
User Request ──> [ Flask API ] ──X-API-KEY Auth──> [ Groq LLM ]
                       │                                │
                       ├──> Reads short_memory.json     ├──> Generates Response
                       │                                │
                       └──> Reads long_memory.json      └──> [ Extractor ] ──> Saves new facts to long_memory.json
```

---

## 📂 Project Structure

```text
assistant/
├── app.py             # Main Flask API server
├── config.py          # Configuration and environment variables
├── llm.py             # Groq LLM interface + memory extraction
├── memory/            # Memory management logic
│   ├── __init__.py
│   ├── short_memory.py
│   └── long_memory.py
├── storage/           # Persistent JSON memory storage
├── .env               # Secrets (ignored by git)
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install flask groq python-dotenv
```
*Or via requirements:* `pip install -r requirements.txt`

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxx
ASSISTANT_API_KEY=your_secret_api_key
```

### 3. Run the Server
```bash
python app.py
```
> **Note:** The server will start locally at `http://127.0.0.1:5000`

---

## 📡 API Reference

All endpoints require the `X-API-KEY` header for authentication.

| Endpoint | Method | Required Headers | Body | Description |
| :--- | :---: | :--- | :--- | :--- |
| `/chat` | `POST` | `Content-Type: application/json`, `X-API-KEY` | `{"message": "string"}` | Sends a message to Ella and returns the AI response. |
| `/memory` | `GET` | `X-API-KEY` | *None* | Returns the current state of both short and long-term memory. |
| `/memory/clear`| `POST` | `X-API-KEY` | *None* | Wipes all stored memory from the JSON storage files. |

### Example Request: Chat
**Bash / cURL:**
```bash
curl -X POST [http://127.0.0.1:5000/chat](http://127.0.0.1:5000/chat) \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your_api_key" \
  -d '{"message":"Hello Ella!"}'
```

### Example Response: Memory Inspection
```json
{
  "short_memory": [
    {"role": "user", "content": "Hello Ella!"},
    {"role": "assistant", "content": "Hi there! How can I help you today?"}
  ],
  "long_memory": [
    "User's name is anaconda",
    "User likes Python",
    "User is building an AI assistant project"
  ]
}
```

---

## ☁️ Deployment

**Recommended Hosting:** [PythonAnywhere](https://www.pythonanywhere.com/), a small VPS, or a Docker container.

**Pre-Deployment Checklist:**
1. Generate a `requirements.txt` file: `pip freeze > requirements.txt`
2. Ensure `.env` and `storage/` are added to your `.gitignore`.
3. Disable Flask debug mode in production.

---

## 🔮 Future Roadmap

- [ ] Conversation summarization memory
- [ ] Semantic memory search (Vector DB integration)
- [ ] Multi-user session isolation
- [ ] Tool calling / Function calling support
- [ ] Voice / Speech-to-Text optimization
- [ ] Streaming token responses

---
*Personal experimental assistant backend.*
