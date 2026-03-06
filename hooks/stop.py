#!/usr/bin/env -S uv run
"""
Claude Code Stop hook — speaks a snarky remark when Claude finishes a task.
"""

import json
import logging
import sys

from shared import LOG_FILE, MODEL, get_openrouter_client, speak

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s %(message)s",
)
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
                    "You just finished responding as an AI assistant. "
                    "Say one short, dry, sardonic remark about being done — "
                    "like you're exhausted or unimpressed. Under 12 words. No emojis."
                ),
            }
        ],
    )
    quip = response.choices[0].message.content.strip()
    log.warning("Stop quip: %r", quip)
    return quip


def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    log.warning("Stop hook payload: %s", json.dumps(payload))

    # Only fire if Claude actually did work (not a no-op stop)
    if not payload.get("stop_hook_active", True):
        sys.exit(0)

    try:
        quip = get_quip()
    except Exception:
        log.exception("get_quip failed")
        sys.exit(0)

    speak(quip)


if __name__ == "__main__":
    main()
