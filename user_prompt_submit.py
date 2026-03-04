#!/opt/homebrew/bin/python3.13
"""
Claude Code UserPromptSubmit hook — roasts the user's prompt via TTS.
Generates a sharp/critical comment using an LLM, then speaks it via pocket-tts.
Falls back to macOS `say` if pocket-tts is unavailable.
"""

import json
import subprocess
import sys

MODEL = "anthropic/claude-haiku-4-5"
VOICE = "hf://kyutai/tts-voices/alba-mackenna/casual.wav"


def get_roast(prompt: str) -> str:
    import os
    from pathlib import Path

    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv(Path(__file__).parent / ".env")

    client = OpenAI(
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
    )
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
    return response.choices[0].message.content.strip()


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
        speak_say(text)


def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = payload.get("prompt", "").strip()
    if not prompt:
        sys.exit(0)

    try:
        roast = get_roast(prompt)
    except Exception:
        roast = prompt

    speak(roast)


if __name__ == "__main__":
    main()
