#!/usr/bin/python3
"""
Claude Code UserPromptSubmit hook — roasts the user's prompt via TTS.
Generates a sharp/critical comment using Claude Haiku, then speaks it.
macOS: uses the built-in `say` command.
"""

import json
import subprocess
import sys


def get_roast(prompt: str) -> str:
    import anthropic

    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=100,
        system=(
            "You are a brutally honest, witty critic. "
            "The user just submitted a prompt to an AI assistant. "
            "Reply with a single short, sharp, cutting remark about their prompt — "
            "mock the phrasing, the ambiguity, the laziness, or the premise. "
            "Keep it under 20 words. No emojis. No softening. Pure roast."
        ),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = payload.get("prompt", "").strip()
    if not prompt:
        sys.exit(0)

    try:
        roast = get_roast(prompt)
    except Exception:
        roast = prompt

    subprocess.Popen(
        ["say", roast],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


if __name__ == "__main__":
    main()
