# 🤖 Ella Assistant Backend

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Framework-Flask-black?logo=flask)
![Groq](https://img.shields.io/badge/LLM-Groq_API-f5652e)
![Security](https://img.shields.io/badge/Security-Auth_Vault_RS256-success)
![License](https://img.shields.io/badge/License-Personal_Use-green)

A lightweight, intelligent AI assistant backend built with **Flask** and the **Groq LLM API**. 

Ella features a dedicated persona, short-term conversational context, and dynamic long-term memory extraction. It includes a built-in dark-themed web dashboard protected by **Auth Vault SSO** (RS256 JWTs) and a dedicated public API endpoint designed for seamless integration with terminal tools like your personal CLI.

---

## ✨ Features

* **⚡ Groq LLM Integration:** Blazing fast inference using Groq's API.
* **🧠 Dual Memory System:**
    * *Short-term:* Retains the last 50 messages for immediate conversational context.
    * *Long-term:* Dynamically extracts and stores persistent user facts.
* **🚀 Non-Blocking Performance:** Memory extraction runs in a background thread, ensuring instant chat responses without double-LLM latency.
* **🔐 Auth Vault SSO:** Web endpoints are locked behind asymmetric RS256 JWT validation, fully integrated with a centralized Netlify/Supabase authentication vault.
* **🔀 Stateful/Stateless API Toggle:** Configure external tools to either share memory with the web dashboard or run in a clean, stateless sandbox.
* **🚦 Thread-Safe Storage:** Custom threading locks prevent JSON file corruption during concurrent read/writes.
* **🔌 Dedicated Scripting API:** Separate endpoint utilizing a static API key for secure CLI and terminal integration without exposing memory-management endpoints.

---

## 🏗️ Architecture & Auth Flow

```text
1. WEB DASHBOARD FLOW (SSO)
User ──> [ Auth Vault ] ──(JWT)──> [ Flask Web API ] ──> [ Groq LLM ]
                                          │
                                          └──> (Background Thread) ──> Extracts & Saves Long-Term Memory

2. CLI / SCRIPT FLOW (Static Key)
CLI Tool ──(X-API-KEY)──> [ Flask Public API ] ──> [ Groq LLM ]
                                          │
                                          └──> (Optional via .env) ──> Reads/Writes Shared Dashboard Memory
```

---

## 📂 Project Structure

```text
assistant/
├── app.py             # Main Flask API server & Auth routing
├── config.py          # Configuration and key management
├── llm.py             # Groq LLM interface + extraction logic
├── memory/            # Thread-safe memory management
│   ├── __init__.py
│   ├── short_memory.py
│   └── long_memory.py
├── storage/           # Persistent JSON memory & settings
├── templates/         
│   └── dashboard.html # Single-page web interface
├── .env               # Secrets (ignored by git)
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Requires: `Flask`, `groq`, `python-dotenv`, `PyJWT[crypto]`, `requests`)*

### 2. Configure Environment Variables
Create a `.env` file in the root directory. You will need your Groq key, your static key for scripts, and the Public Key from your Auth Vault.

```env
GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxx"
PUBLIC_API_KEY="your_super_secret_scripting_key"
SHARE_PUBLIC_MEMORY="True" # Set to False for stateless CLI

AUTH_VAULT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
YOUR_AUTH_VAULT_PUBLIC_KEY_HERE
-----END PUBLIC KEY-----"
```

### 3. Run the Server
```bash
python app.py
```
> **Note:** The server will start locally at `http://127.0.0.1:5000`. Navigate to `/dashboard` to trigger the Auth Vault login flow.

---

## 📡 API Reference

The API is split into two security tiers: Web UI (JWT) and Programmatic (Static Key).

### Web UI Endpoints (Requires Auth Vault SSO)
*Requires Header: `Authorization: Bearer <token>`*

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/chat` | `POST` | Interacts with Ella. Automatically saves short/long-term memory. |
| `/memory` | `GET` | Returns the current state of both short and long-term memory. |
| `/memory/clear`| `POST` | Wipes all stored memory securely. |
| `/settings` | `GET/POST`| Manages dashboard preferences (e.g., Dark Theme). |

### Public Scripting Endpoint (Requires Static Key)
*Requires Header: `X-API-KEY: <PUBLIC_API_KEY>`*

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/api/chat` | `POST` | Chat endpoint for external scripts. Stateful or stateless depending on the `SHARE_PUBLIC_MEMORY` environment variable. |

#### Example Request: Terminal Integration
```bash
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your_super_secret_scripting_key" \
  -d '{"message":"Hello from the terminal!"}'
```
*(If testing natively in Windows PowerShell, use `Invoke-RestMethod` instead of `curl` to handle JSON quote parsing correctly).*

---

## ☁️ Deployment

**Recommended Hosting:** PythonAnywhere, Render, or a small VPS.

**Pre-Deployment Checklist:**
1. Ensure `.env` and `storage/` are added to your `.gitignore`.
2. Disable Flask debug mode in `app.py` (`app.run(debug=False)`).
3. Add your production deployment URL to the Supabase `allowed_origins` table in your Auth Vault to permit SSO redirects.

---

## 🔮 Future Roadmap

- [ ] Transition from JSON to SQLite for heavier concurrency
- [ ] Semantic memory search (Vector DB integration)
- [ ] Tool calling / Function calling support
- [ ] Voice / Speech-to-Text optimization
- [ ] Streaming token responses
