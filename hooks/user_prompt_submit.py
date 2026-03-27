#!/usr/bin/env -S uv run
# /// script
# dependencies = ["openai", "python-dotenv", "pocket-tts", "sounddevice"]
# ///
"""
Claude Code UserPromptSubmit hook — roasts the user's prompt via TTS.
Generates a sharp/critical comment using an LLM, then speaks it via pocket-tts.
Falls back to macOS `say` if pocket-tts is unavailable.
"""

import json
import logging
import sys

from shared import (
    MODEL,
    detach,
    get_openrouter_client,
    get_personality,
    is_enabled,
    setup_logging,
    speak,
)

setup_logging()
log = logging.getLogger(__name__)


def get_roast(prompt: str) -> str:
    client = get_openrouter_client()
    personality = get_personality()
    log.debug("Requesting roast for prompt: %r", prompt[:80])
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=100,
        messages=[
            {"role": "system", "content": personality["prompt_submit"]},
            {"role": "user", "content": prompt},
        ],
    )
    roast = response.choices[0].message.content.strip()
    log.debug("Roast: %r", roast)
    return roast


def main():
    log.info("User prompt submit hook triggered")
    try:
        payload = json.load(sys.stdin)
        log.debug("Payload: %r", payload)

        if not is_enabled():
            sys.exit(0)
    except json.JSONDecodeError:
        log.warning("Invalid JSON payload, exiting")
        sys.exit(0)

    prompt = payload.get("prompt", "").strip()
    if not prompt:
        sys.exit(0)

    detach()

    log.debug("Getting roast and speaking")
    try:
        roast = get_roast(prompt)
    except Exception:
        log.exception("get_roast failed, speaking raw prompt")
        roast = prompt

    speak(roast)


if __name__ == "__main__":
    main()
