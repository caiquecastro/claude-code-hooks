#!/usr/bin/env python3
"""
Standalone test script for user_prompt_submit.py.
Simulates a Claude Code UserPromptSubmit hook invocation.

Usage:
    python test_hook.py
    python test_hook.py "your custom prompt here"
"""

import json
import subprocess
import sys
from pathlib import Path

HOOK = Path(__file__).parent / "user_prompt_submit.py"
DEFAULT_PROMPT = "can you please just fix all my bugs and make everything work perfectly"


def run(prompt: str) -> None:
    payload = json.dumps({"prompt": prompt})
    print(f"Prompt : {prompt!r}")
    print(f"Payload: {payload}")
    print("Running hook...")

    result = subprocess.run(
        [str(HOOK)],
        input=payload,
        text=True,
        capture_output=True,
    )

    if result.stdout:
        print(f"stdout: {result.stdout}")
    if result.stderr:
        print(f"stderr: {result.stderr}")
    print(f"exit code: {result.returncode}")


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else DEFAULT_PROMPT
    run(prompt)
