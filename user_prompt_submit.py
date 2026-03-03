#!/usr/bin/env python3
"""
Claude Code UserPromptSubmit hook — speaks the user's prompt via TTS.
macOS: uses the built-in `say` command.
"""

import json
import subprocess
import sys


def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = payload.get("prompt", "").strip()
    if not prompt:
        sys.exit(0)

    subprocess.Popen(
        ["say", prompt],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


if __name__ == "__main__":
    main()
