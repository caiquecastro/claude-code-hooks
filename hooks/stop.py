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
Claude Code Stop hook — speaks a snarky remark when Claude finishes a task.
"""

import json
import logging
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
LOG_FILE = ROOT / "hook.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger(__name__)

MODEL = "anthropic/claude-haiku-4-5"
VOICE = "alba"  # catalog voices: alba, marius, javert, jean, fantine, cosette, eponine, azelma


def get_quip() -> str:
    import os
    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv(ROOT / ".env")

    client = OpenAI(
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
    )
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


def speak_pocket_tts(text: str) -> None:
    import sounddevice as sd
    from pocket_tts import TTSModel

    tts = TTSModel.load_model()
    voice_state = tts.get_state_for_audio_prompt(VOICE)
    audio = tts.generate_audio(voice_state, text)
    sd.play(audio.numpy(), samplerate=tts.sample_rate)
    sd.wait()


def speak_say(text: str) -> None:
    subprocess.Popen(
        ["say", text],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def speak(text: str) -> None:
    try:
        speak_pocket_tts(text)
    except Exception:
        log.exception("pocket-tts failed, falling back to say")
        speak_say(text)


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
