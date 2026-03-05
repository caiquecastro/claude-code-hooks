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
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
LOG_FILE = ROOT / "hook.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger(__name__)

MODEL = "anthropic/claude-haiku-4-5"
VOICE = "alba"  # catalog voices: alba, marius, javert, jean, fantine, cosette, eponine, azelma


def get_roast(prompt: str) -> str:
    import os
    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv(ROOT / ".env")

    client = OpenAI(
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
    )
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


def speak_pocket_tts(text: str) -> None:
    import sounddevice as sd
    from pocket_tts import TTSModel

    log.debug("Speaking via pocket-tts")
    tts = TTSModel.load_model()
    voice_state = tts.get_state_for_audio_prompt(VOICE)
    audio = tts.generate_audio(voice_state, text)
    sd.play(audio.numpy(), samplerate=tts.sample_rate)
    sd.wait()


def speak_say(text: str) -> None:
    log.debug("Speaking via say")
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
