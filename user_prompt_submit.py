#!/usr/bin/python3
"""
Claude Code UserPromptSubmit hook — roasts the user's prompt via TTS.
Generates a sharp/critical comment using Claude Haiku, then speaks it.
macOS: uses the built-in `say` command.
"""

import json
import subprocess
import sys


MODEL = "anthropic/claude-haiku-4-5"


def get_roast(prompt: str) -> str:
    import os
    from pathlib import Path

    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv(Path(__file__).parent / ".env")

    client = OpenAI(
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
    )
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=100,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a brutally honest, witty critic. "
                    "The user just submitted a prompt to an AI assistant. "
                    "Reply with a single short, sharp, cutting remark about their prompt — "
                    "mock the phrasing, the ambiguity, the laziness, or the premise. "
                    "Keep it under 20 words. No emojis. No softening. Pure roast."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()


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
    except Exception as e:
        print(e)
        roast = prompt

    subprocess.Popen(
        ["say", roast],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


if __name__ == "__main__":
    main()
