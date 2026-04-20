# E.L.E.N.A AI

**Enhanced Linguistic Engine for Natural Assistance**

[![Python](https://img.shields.io/badge/python-≥3.11-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![OpenRouter](https://img.shields.io/badge/powered%20by-OpenRouter-orange)](https://openrouter.ai)

Terminal-based AI assistant with persistent session memory, async streaming, and auto-compaction — inspired by [nanobot](https://github.com/HKUDS/nanobot) architecture.

---

## Features

- **Async streaming** — token-by-token output via Rich Live renderer, zero flicker
- **Persistent sessions** — conversation history survives restarts (`session.json`)
- **Auto-compaction** — when history exceeds threshold, older turns are summarized and compressed (nanobot pattern)
- **Model-agnostic** — any model available on OpenRouter, switchable at runtime
- **Minimal deps** — only `httpx` + `rich`

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/suryadi346-star/elena-ai.git
cd elena-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set API key

Get a free key at [openrouter.ai/keys](https://openrouter.ai/keys).

```bash
# Option A: environment variable (recommended)
export OPENROUTER_API_KEY="sk-or-v1-..."

# Option B: key file (auto-created on first run)
echo "sk-or-v1-..." > key.txt
```

### 4. Run

```bash
python main.py
```

---

## Commands

| Command | Description |
|---|---|
| `/help` | Show all commands |
| `/reset` | Clear conversation history |
| `/model` | Show current model |
| `/model <name>` | Switch model (e.g. `/model openai/gpt-4o`) |
| `/history` | Show last 20 messages |
| `/status` | Session stats (message count, memory, model) |
| `/clear` | Clear terminal |
| `exit` / `quit` / `:q` | Quit |

---

## Model Recommendations

| Use Case | Model |
|---|---|
| Default (fast + cheap) | `deepseek/deepseek-chat` |
| Higher quality | `anthropic/claude-sonnet-4-5` |
| Best reasoning | `openai/gpt-4o` |
| Local/free | `mistralai/mistral-7b-instruct` |

---

## Project Structure

```
elena-ai/
├── elena.py          # Core engine: Session, Provider, Agent, StreamRenderer
├── main.py           # CLI entry point: REPL, banner, command routing
├── requirements.txt  # httpx, rich
├── key.txt           # API key (auto-created, gitignored)
├── session.json      # Persistent conversation history (auto-created)
└── memory.md         # Optional: manual memory notes read at startup
```

---

## Architecture

```
main.py  ──►  ElenaAgent.chat(input)
                  │
                  ├─ Session.get_context_messages()   # unconsolidated tail
                  ├─ _maybe_compact()                 # autocompact if needed
                  ├─ _build_messages()                # system + summary + history + input
                  │
                  └─ OpenRouterProvider.stream_chat()
                            │
                            ▼
                       StreamRenderer (Rich Live)
                            │
                            ▼
                       Session.add() → Session.save()
```

**Autocompact flow** (mirrors nanobot's `AutoCompact`):
- Threshold: 30 unconsolidated messages
- Older turns are summarized via a separate LLM call
- Summary injected as context prefix in next prompts
- Recent 8 messages retained verbatim

---

## Configuration

Edit constants at the top of `elena.py`:

```python
DEFAULT_MODEL          = "deepseek/deepseek-chat"
MAX_HISTORY_MESSAGES   = 40    # hard cap on total stored messages
AUTOCOMPACT_THRESHOLD  = 30    # compact trigger
RECENT_KEEP            = 8     # messages kept after compact
MAX_TOKENS             = 4096  # max response tokens
STREAM_REFRESH_RATE    = 0.12  # Rich Live refresh interval (seconds)
```

---

## Requirements

- Python ≥ 3.11
- `httpx >= 0.27.0`
- `rich >= 13.7.0`
- OpenRouter API key

Works on Linux, macOS, Windows, and Termux (Android).

---

## License

MIT — see [LICENSE](LICENSE)

---

*Dev: Suryadi · Architecture reference: [HKUDS/nanobot](https://github.com/HKUDS/nanobot)*
