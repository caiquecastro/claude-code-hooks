#!/usr/bin/env python3
"""
Standalone test script for task_completed.py.
Simulates a Claude Code TaskCompleted hook invocation.

Usage:
    python test_task_completed.py
"""

import json
import subprocess
import sys
from pathlib import Path

HOOK = Path(__file__).parent / "task_completed.py"


def run() -> None:
    payload = json.dumps({})
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
    run()
