"""
E.L.E.N.A AI — v4.0
Enhanced Linguistic Engine for Natural Assistance
Inspired by nanobot (HKUDS/nanobot) architecture.
Dev: Suryadi
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncIterator

import httpx
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

# ─────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────

APP_NAME    = "E.L.E.N.A"
VERSION     = "4.0"
AUTHOR      = "Suryadi"
API_URL     = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "deepseek/deepseek-chat"

BASE_DIR      = Path(__file__).parent
KEY_FILE      = BASE_DIR / "key.txt"
SESSION_FILE  = BASE_DIR / "session.json"
MEMORY_FILE   = BASE_DIR / "memory.md"

MAX_HISTORY_MESSAGES = 40    # hard cap kept in session
AUTOCOMPACT_THRESHOLD = 30   # compact when unconsolidated turns exceed this
RECENT_KEEP = 8              # messages retained after compaction
MAX_TOKENS  = 4096
STREAM_REFRESH_RATE = 0.12   # seconds between Live refreshes

PERSONA = """You are E.L.E.N.A (Enhanced Linguistic Engine for Natural Assistance), an AI assistant created by Suryadi.

Core traits:
- Direct, precise, and technically sharp.
- Adapt language to the user (Indonesian or English, match their register).
- Never add empty filler phrases or unnecessary disclaimers.
- If uncertain, say so explicitly rather than guessing.
- Identity: developed by Suryadi, powered by OpenRouter.
"""

# ─────────────────────────────────────────
#  COLORS (Rich-free fallback for banner)
# ─────────────────────────────────────────

class C:
    R     = "\033[31m"
    G     = "\033[32m"
    Y     = "\033[33m"
    B     = "\033[34m"
    M     = "\033[35m"
    CY    = "\033[36m"
    W     = "\033[37m"
    BOLD  = "\033[1m"
    DIM   = "\033[2m"
    RESET = "\033[0m"


# ─────────────────────────────────────────
#  SESSION  (nanobot-inspired)
# ─────────────────────────────────────────

@dataclass
class Session:
    messages: list[dict[str, Any]] = field(default_factory=list)
    last_consolidated: int = 0          # index up to which memory is compacted
    summary: str = ""                   # rolling summary from autocompact
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    # ── persistence ──────────────────────

    def save(self) -> None:
        SESSION_FILE.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False))

    def to_dict(self) -> dict:
        return {
            "messages": self.messages,
            "last_consolidated": self.last_consolidated,
            "summary": self.summary,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def load(cls) -> "Session":
        if SESSION_FILE.exists():
            try:
                data = json.loads(SESSION_FILE.read_text())
                return cls(**data)
            except Exception:
                pass
        return cls()

    # ── history window ───────────────────

    def get_context_messages(self) -> list[dict[str, Any]]:
        """Return only the unconsolidated tail, aligned to a user-turn boundary."""
        tail = self.messages[self.last_consolidated:]
        # align to first user message so we never start mid-turn
        for i, m in enumerate(tail):
            if m["role"] == "user":
                tail = tail[i:]
                break
        return [{"role": m["role"], "content": m["content"]} for m in tail]

    def add(self, role: str, content: str) -> None:
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        })
        self.updated_at = datetime.now().isoformat()

    def clear(self) -> None:
        self.messages.clear()
        self.last_consolidated = 0
        self.summary = ""
        self.updated_at = datetime.now().isoformat()

    # ── autocompact (nanobot pattern) ────

    def needs_compaction(self) -> bool:
        unconsolidated = len(self.messages) - self.last_consolidated
        return unconsolidated >= AUTOCOMPACT_THRESHOLD

    def compact(self, summary: str) -> None:
        """Keep only recent N messages, store summary."""
        tail = self.messages[self.last_consolidated:]
        # keep last RECENT_KEEP, aligned to a user boundary
        kept = tail[-RECENT_KEEP:]
        for i, m in enumerate(kept):
            if m["role"] == "user":
                kept = kept[i:]
                break
        self.messages = self.messages[:self.last_consolidated] + kept
        self.last_consolidated = len(self.messages)
        self.summary = summary
        self.updated_at = datetime.now().isoformat()


# ─────────────────────────────────────────
#  LLM PROVIDER  (async, streaming)
# ─────────────────────────────────────────

class OpenRouterProvider:
    def __init__(self, api_key: str, model: str = DEFAULT_MODEL):
        self.api_key = api_key
        self.model   = model

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/suryadi346-star/elena-ai",
            "X-Title": APP_NAME,
        }

    def _payload(self, messages: list[dict], stream: bool = True) -> dict:
        return {
            "model": self.model,
            "messages": messages,
            "max_tokens": MAX_TOKENS,
            "temperature": 0.7,
            "stream": stream,
        }

    async def stream_chat(self, messages: list[dict]) -> AsyncIterator[str]:
        """Yield text deltas as they arrive."""
        async with httpx.AsyncClient(timeout=90) as client:
            async with client.stream(
                "POST", API_URL,
                headers=self._headers(),
                json=self._payload(messages, stream=True),
            ) as resp:
                if resp.status_code != 200:
                    body = await resp.aread()
                    raise RuntimeError(f"HTTP {resp.status_code}: {body.decode()[:300]}")

                async for raw in resp.aiter_lines():
                    if not raw or not raw.startswith("data: "):
                        continue
                    data = raw[6:]
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                        delta = chunk["choices"][0].get("delta", {}).get("content", "")
                        if delta:
                            yield delta
                    except (json.JSONDecodeError, KeyError, IndexError):
                        continue

    async def summarize(self, messages: list[dict]) -> str:
        """One-shot call to produce a compact summary for autocompact."""
        prompt = (
            "Summarize the following conversation into a short, dense memory block "
            "(max 200 words). Preserve key facts, decisions, and user preferences.\n\n"
        )
        for m in messages:
            prompt += f"[{m['role'].upper()}]: {m['content']}\n"

        payload = self._payload([
            {"role": "system", "content": "You are a concise summarizer. Respond only with the summary."},
            {"role": "user", "content": prompt},
        ], stream=False)

        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(API_URL, headers=self._headers(), json=payload)
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()


# ─────────────────────────────────────────
#  STREAM RENDERER  (nanobot-inspired Rich)
# ─────────────────────────────────────────

class StreamRenderer:
    """Rich Live renderer for streaming tokens — flicker-free."""

    def __init__(self, console: Console):
        self._console = console
        self._buf = ""
        self._live: Live | None = None
        self._t = 0.0
        self.streamed = False

    def _render(self):
        return Markdown(self._buf) if self._buf.strip() else Text("")

    def start(self) -> None:
        self._buf = ""
        self._live = None
        self._t = 0.0
        self.streamed = False

    async def on_delta(self, delta: str) -> None:
        self.streamed = True
        self._buf += delta
        if self._live is None:
            if not self._buf.strip():
                return
            self._console.print()
            self._console.print(f"[bold cyan]◈ {APP_NAME}[/bold cyan]")
            self._live = Live(
                self._render(),
                console=self._console,
                auto_refresh=False,
            )
            self._live.start()
        now = time.monotonic()
        if (now - self._t) > STREAM_REFRESH_RATE:
            self._live.update(self._render())
            self._live.refresh()
            self._t = now

    def finish(self) -> str:
        if self._live:
            self._live.update(self._render())
            self._live.refresh()
            self._live.stop()
            self._live = None
        self._console.print()
        return self._buf


# ─────────────────────────────────────────
#  AGENT LOOP
# ─────────────────────────────────────────

class ElenaAgent:
    def __init__(self, api_key: str, model: str = DEFAULT_MODEL):
        self.provider = OpenRouterProvider(api_key, model)
        self.session  = Session.load()
        self.console  = Console()
        self._renderer = StreamRenderer(self.console)

    # ── build prompt ─────────────────────

    def _build_messages(self, user_input: str) -> list[dict]:
        msgs: list[dict] = [{"role": "system", "content": PERSONA}]

        # inject rolling summary as a synthetic user/assistant pair
        if self.session.summary:
            msgs.append({"role": "user",      "content": "[Context from earlier in this session]"})
            msgs.append({"role": "assistant",  "content": self.session.summary})

        msgs.extend(self.session.get_context_messages())
        msgs.append({"role": "user", "content": user_input})
        return msgs

    # ── autocompact ──────────────────────

    async def _maybe_compact(self) -> None:
        if not self.session.needs_compaction():
            return
        self.console.print("[dim]  ⟳ compacting session memory...[/dim]")
        tail = self.session.messages[self.session.last_consolidated:]
        try:
            summary = await self.provider.summarize(tail)
            self.session.compact(summary)
            self.session.save()
        except Exception as e:
            self.console.print(f"[yellow]  ⚠ autocompact failed: {e}[/yellow]")

    # ── main chat call ───────────────────

    async def chat(self, user_input: str) -> str:
        await self._maybe_compact()

        messages = self._build_messages(user_input)
        self.session.add("user", user_input)
        self._renderer.start()

        full_response = ""
        try:
            async for delta in self.provider.stream_chat(messages):
                await self._renderer.on_delta(delta)
                full_response += delta
        except Exception as e:
            self.console.print(f"\n[bold red]Error:[/bold red] {e}")
            self.session.messages.pop()   # remove the user turn we added
            return ""

        full_response = self._renderer.finish()
        self.session.add("assistant", full_response)
        self.session.save()
        return full_response

    # ── command handlers ─────────────────

    def cmd_reset(self) -> str:
        self.session.clear()
        self.session.save()
        return "Session cleared."

    def cmd_model(self) -> str:
        return f"Model: [cyan]{self.provider.model}[/cyan]"

    def cmd_set_model(self, model: str) -> str:
        self.provider.model = model
        return f"Model set to [cyan]{model}[/cyan]"

    def cmd_history(self) -> str:
        msgs = self.session.messages
        if not msgs:
            return "No history."
        lines = []
        for m in msgs[-20:]:
            role  = m["role"].upper()
            ts    = m.get("timestamp", "")[:16]
            snip  = m["content"][:120].replace("\n", " ")
            lines.append(f"[{ts}] {role}: {snip}")
        return "\n".join(lines)

    def cmd_memory(self) -> str:
        if MEMORY_FILE.exists():
            return MEMORY_FILE.read_text()
        return "No memory file found."

    def cmd_status(self) -> str:
        total   = len(self.session.messages)
        unconsc = total - self.session.last_consolidated
        return (
            f"Model:         {self.provider.model}\n"
            f"Messages:      {total}\n"
            f"Unconsolidated:{unconsc}\n"
            f"Has summary:   {'Yes' if self.session.summary else 'No'}\n"
            f"Session file:  {SESSION_FILE}\n"
        )
