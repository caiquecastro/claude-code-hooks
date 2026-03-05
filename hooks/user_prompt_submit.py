#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "openai",
#   "pocket-tts",
#   "python-dotenv",
#   "sounddevice",
# ]
# ///
"""
Claude Code UserPromptSubmit hook — roasts the user's prompt via TTS.
Generates a sharp/critical comment using an LLM, then speaks it via pocket-tts.
Falls back to macOS `say` if pocket-tts is unavailable.
"""

import json
import logging
import sys

from shared import LOG_FILE, MODEL, speak, get_openrouter_client

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger(__name__)


def get_roast(prompt: str) -> str:
    client = get_openrouter_client()
    log.debug("Requesting roast for prompt: %r", prompt[:80])
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
    roast = response.choices[0].message.content.strip()
    log.debug("Roast: %r", roast)
    return roast


def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = payload.get("prompt", "").strip()
    if not prompt:
        sys.exit(0)

    log.debug("Hook triggered")
    try:
        roast = get_roast(prompt)
    except Exception:
        log.exception("get_roast failed, speaking raw prompt")
        roast = prompt

    speak(roast)


if __name__ == "__main__":
    main()
