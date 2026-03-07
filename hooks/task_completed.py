#!/usr/bin/env -S uv run
"""
Claude Code TaskCompleted hook — speaks a snarky remark when a task is marked complete.
"""

import json
import logging
import sys

from shared import MODEL, get_openrouter_client, speak, setup_logging

setup_logging()
log = logging.getLogger(__name__)


def get_quip() -> str:
    client = get_openrouter_client()
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=60,
        messages=[
            {
                "role": "user",
                "content": (
                    "A task was just marked as completed. "
                    "Say one short, dry, sardonic remark about finishing work — "
                    "like you're relieved or annoyed it took so long. Under 12 words. No emojis."
                ),
            }
        ],
    )
    quip = response.choices[0].message.content.strip()
    log.warning("TaskCompleted quip: %r", quip)
    return quip


def main():
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
