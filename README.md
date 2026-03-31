# Local AI PDF RAG Assistant
### Telegram + Ollama + Qwen 2.5 7B — fully local, no API costs

A privacy-first AI assistant that runs entirely on your machine. Send it a PDF via Telegram and ask questions — it answers using only your document content.

---

## What It Does

- **Chat with your PDFs** — upload any PDF via Telegram, ask questions, get answers grounded in the document
- **100% local** — no OpenAI, no cloud APIs, no data leaving your machine
- **Persistent vector store** — PDFs stay indexed between sessions (ChromaDB)
- **Conversational memory** — remembers the last 20 messages in a session

---

## Architecture

```
User (Telegram)
      ↓
Telegram Bot  (python-telegram-bot)
      ↓
Python Backend  (bot.py)
      ↓
Agent Layer  (agent.py — LangChain + Ollama)
      ↓
RAG Pipeline  (rag.py — ChromaDB + nomic-embed-text)
      ↓
Ollama  →  Qwen 2.5 7B  (local LLM)
```

---

## Project Structure

```
ai-rag-bot/
├── bot.py          ← Telegram bot entry point
├── agent.py        ← LLM agent with conversation memory
├── rag.py          ← PDF ingestion + vector search
├── uploads/        ← PDFs saved here after upload (auto-created)
├── chroma_db/      ← Vector database, persists between runs (auto-created)
├── requirements.txt
└── README.md
```

---

## Requirements

- Windows 10/11
- Python 3.10+
- [Ollama](https://ollama.com/download) installed and running
- A Telegram account

---

## Installation

### 1. Clone or download the project

```powershell
cd C:\projects
# place all files in ai-rag-bot\
cd ai-rag-bot
```

### 2. Create and activate virtual environment

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install python-telegram-bot ollama chromadb pypdf langchain-text-splitters langchain-ollama
```

### 4. Pull the required Ollama models

```powershell
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
```

### 5. Create your Telegram bot

1. Open Telegram → search `@BotFather`
2. Send `/newbot` and follow the prompts
3. Copy the token BotFather gives you (looks like `7412345678:AAFxxx...`)

### 6. Add your token to bot.py

Open `bot.py` and replace the token placeholder:

```python
BOT_TOKEN = "7412345678:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

## Running the Bot

```powershell
# Make sure venv is active
.\venv\Scripts\activate

# Start the bot
python bot.py
```

You should see:
```
INFO:telegram.ext.Application: Application started
```

Leave this terminal open — the bot runs as long as this process is alive.

---

## Usage

### Start the bot
Send `/start` to your bot in Telegram.

### Upload a PDF
Tap the paperclip icon in Telegram → select a PDF → send it.
The bot will index it and confirm when ready.

### Ask questions
Send any text message after uploading a PDF:

```
Who is the CEO mentioned in this document?
What are the key findings?
Summarize the introduction.
```

The bot searches the indexed PDF chunks, injects the relevant context into the prompt, and answers using Qwen 2.5 locally.

---

## How RAG Works

1. **Ingest** — PDF text is extracted and split into 500-character chunks (50-char overlap)
2. **Embed** — each chunk is converted to a vector using `nomic-embed-text` via Ollama
3. **Store** — vectors are saved in ChromaDB on disk (`./chroma_db/`)
4. **Query** — your question is embedded and the top 5 most similar chunks are retrieved
5. **Answer** — retrieved chunks are injected into the LLM prompt as context

---

## Dependencies

| Package | Purpose |
|---|---|
| `python-telegram-bot` | Telegram bot framework |
| `ollama` | Python client for local Ollama API |
| `langchain-ollama` | LangChain integration for Ollama LLM |
| `langchain-text-splitters` | Chunking text for RAG |
| `chromadb` | Local vector database |
| `pypdf` | PDF text extraction |

---

## Troubleshooting

**Bot doesn't start — Invalid token**
→ Make sure you pasted your real BotFather token in `bot.py`, not the placeholder text.

**`nomic-embed-text` error during PDF upload**
→ Run `ollama pull nomic-embed-text` in a new terminal window.

**Ollama connection error**
→ Make sure Ollama is running. Open a terminal and run `ollama list` to verify.

**Bot crashes on large PDFs**
→ Large PDFs take longer to embed. Watch the terminal for progress logs.

**Wrong or hallucinated answers**
→ Make sure you uploaded a PDF first. Without indexed documents, the bot has no context to search.

---

## Next Steps / Roadmap

- [ ] Add PostgreSQL + pgvector for persistent memory across users
- [ ] Enable streaming responses (token by token output)
- [ ] Add tool calling (web search, database queries)
- [ ] Support multiple PDFs and per-user document isolation
- [ ] Add a `/list` command to show indexed documents
- [ ] Add a `/clear` command to wipe the vector store

---

## Credits

Built with [Ollama](https://ollama.com), [Qwen 2.5](https://huggingface.co/Qwen), [ChromaDB](https://www.trychroma.com), [LangChain](https://langchain.com), and [python-telegram-bot](https://python-telegram-bot.org).

Inspired by the local LLM stack movement — AI systems that respect your privacy.
