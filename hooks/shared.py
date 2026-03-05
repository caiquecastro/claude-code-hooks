"""
Shared utilities for Claude Code hooks.
"""

import logging
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
LOG_FILE = ROOT / "hook.log"

MODEL = "anthropic/claude-haiku-4-5"
VOICE = "alba"  # catalog voices: alba, marius, javert, jean, fantine, cosette, eponine, azelma

log = logging.getLogger(__name__)


def get_openrouter_client():
    import os
    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv(ROOT / ".env")
    return OpenAI(
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
    )


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
