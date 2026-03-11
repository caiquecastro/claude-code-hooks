#!/usr/bin/env -S uv run
# /// script
# dependencies = ["openai", "python-dotenv", "pocket-tts", "sounddevice"]
# ///
"""
Claude Code TaskCompleted hook — speaks a snarky remark when a task is marked complete.
"""

import json
import logging
import sys

from shared import MODEL, get_openrouter_client, get_personality, is_enabled, speak, setup_logging

setup_logging()
log = logging.getLogger(__name__)


def get_quip() -> str:
    client = get_openrouter_client()
    personality = get_personality()
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=60,
        messages=[{"role": "user", "content": personality["task_completed"]}],
    )
    quip = response.choices[0].message.content.strip()
    log.warning("TaskCompleted quip: %r", quip)
    return quip


def main():
    if not is_enabled():
        sys.exit(0)
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    log.warning("TaskCompleted hook payload: %s", json.dumps(payload))

    try:
        quip = get_quip()
    except Exception:
        log.exception("get_quip failed")
        sys.exit(0)

    speak(quip)


if __name__ == "__main__":
    main()
