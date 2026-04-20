"""
E.L.E.N.A AI — CLI entry point
Run: python main.py
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from elena import (
    APP_NAME, VERSION, AUTHOR, DEFAULT_MODEL,
    KEY_FILE, ElenaAgent, C,
)

console = Console()

BANNER = f"""
{C.B}{C.BOLD}
    ███████╗██╗     ███████╗███╗   ██╗ █████╗
    ██╔════╝██║     ██╔════╝████╗  ██║██╔══██╗
    █████╗  ██║     █████╗  ██╔██╗ ██║███████║
    ██╔══╝  ██║     ██╔══╝  ██║╚██╗██║██╔══██║
    ███████╗███████╗███████╗██║ ╚████║██║  ██║
    ╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝
{C.CY}    v{VERSION}  ·  Dev: {AUTHOR}  ·  Powered by OpenRouter{C.RESET}
"""

HELP_TEXT = """
[bold cyan]Commands:[/bold cyan]
  /help             Show this message
  /reset            Clear conversation history
  /model            Show current model
  /model <name>     Switch model  (e.g. /model openai/gpt-4o)
  /history          Show last 20 messages
  /status           Show session stats
  /clear            Clear terminal
  exit | quit | :q  Quit
"""


def print_banner() -> None:
    print(BANNER)


def load_or_prompt_key() -> str:
    # 1. environment variable
    key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if key:
        return key
    # 2. key file
    if KEY_FILE.exists():
        key = KEY_FILE.read_text().strip()
        if key:
            return key
    # 3. prompt
    console.print(f"[yellow]No API key found.[/yellow]")
    key = input("Enter your OpenRouter API key: ").strip()
    if not key:
        sys.exit(f"{C.R}Aborted — no API key provided.{C.RESET}")
    KEY_FILE.write_text(key)
    console.print(f"[green]Key saved to {KEY_FILE}[/green]")
    return key


async def repl(agent: ElenaAgent) -> None:
    prompt_str = f"{C.W}{C.BOLD}E{C.R}·{C.W}L{C.R}·{C.W}E{C.R}·{C.W}N{C.R}·{C.W}A{C.RESET} ❯ "

    while True:
        try:
            user_input = input(prompt_str).strip()
        except (KeyboardInterrupt, EOFError):
            console.print(f"\n[yellow]Session ended.[/yellow]")
            break

        if not user_input:
            continue

        # ── exit ─────────────────────────────
        if user_input.lower() in {"exit", "quit", ":q"}:
            console.print("[yellow]Shutting down…[/yellow]")
            break

        # ── commands ─────────────────────────
        if user_input.startswith("/"):
            parts = user_input.split(None, 1)
            cmd   = parts[0].lower()
            arg   = parts[1] if len(parts) > 1 else ""

            if cmd == "/help":
                console.print(Panel(HELP_TEXT, title="Help", border_style="cyan"))
            elif cmd == "/reset":
                console.print(f"[green]{agent.cmd_reset()}[/green]")
            elif cmd == "/model":
                if arg:
                    console.print(f"[green]{agent.cmd_set_model(arg)}[/green]")
                else:
                    console.print(agent.cmd_model())
            elif cmd == "/history":
                console.print(agent.cmd_history())
            elif cmd == "/status":
                console.print(Panel(agent.cmd_status(), title="Status", border_style="dim"))
            elif cmd == "/clear":
                os.system("cls" if os.name == "nt" else "clear")
            else:
                console.print(f"[yellow]Unknown command: {cmd}. Type /help.[/yellow]")
            continue

        # ── chat ─────────────────────────────
        await agent.chat(user_input)


def main() -> None:
    print_banner()
    api_key = load_or_prompt_key()
    agent   = ElenaAgent(api_key=api_key, model=DEFAULT_MODEL)
    console.print(f"[dim]Session loaded · {len(agent.session.messages)} messages in history[/dim]")
    console.print(f"[dim]Type [bold]/help[/bold] for commands · [bold]exit[/bold] to quit[/dim]\n")
    asyncio.run(repl(agent))


if __name__ == "__main__":
    main()
