# Cursed Hooks

A collection of hooks for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and [Codex](https://github.com/openai/codex) that do things you probably shouldn't do.

Both tools share the same hook format, so these hooks work with either one out of the box.

## Hooks

### `hooks/user_prompt_submit.py` — Prompt roaster

A `UserPromptSubmit` hook that intercepts every prompt you send, calls an LLM to generate a sharp/critical remark about it, and reads it aloud via TTS.

### `hooks/stop.py` — Task complete quip

A `Stop` hook that fires when the agent finishes responding, generating a dry sardonic one-liner and reading it aloud.

### `hooks/task_completed.py` — Task done quip

A `TaskCompleted` hook that fires when a task is marked as complete, generating a sardonic remark about finishing work and reading it aloud.

All hooks use [pocket-tts](https://github.com/kyutai-labs/pocket-tts) for high-quality local TTS, with macOS `say` as a fallback.

## Requirements

- macOS
- [uv](https://docs.astral.sh/uv/) — manages Python dependencies automatically
- An [OpenRouter](https://openrouter.ai) API key

## Setup

### 1. Install uv

```sh
brew install uv
```

### 2. Configure your API key

Create a `.env` file in the repo root:

```sh
echo 'OPENROUTER_API_KEY=sk-or-...' > .env
```

### 3. Register the hooks

#### Claude Code

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/cursed-hooks/hooks/user_prompt_submit.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/cursed-hooks/hooks/stop.py"
          }
        ]
      }
    ],
    "TaskCompleted": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/cursed-hooks/hooks/task_completed.py"
          }
        ]
      }
    ]
  }
}
```

#### Codex

Add to `.codex/hooks.json` in your project root:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/cursed-hooks/hooks/user_prompt_submit.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/cursed-hooks/hooks/stop.py"
          }
        ]
      }
    ]
  }
}
```

Replace `/path/to/cursed-hooks` with the actual path to this repo.

Dependencies are installed automatically by `uv` on first run (this may take a moment as it downloads the TTS model weights).

## Configuration

At the top of each hook script:

| Constant | Description |
|----------|-------------|
| `MODEL`  | OpenRouter model ID for generating remarks (default: `anthropic/claude-haiku-4-5`) |
| `VOICE`  | pocket-tts catalog voice (default: `alba`) |

Available voices: `alba`, `marius`, `javert`, `jean`, `fantine`, `cosette`, `eponine`, `azelma`

## Testing

```sh
# Test the UserPromptSubmit hook
python hooks/test_user_prompt_submit.py
python hooks/test_user_prompt_submit.py "your prompt here"

# Test the Stop hook
python hooks/test_stop.py

# Test the TaskCompleted hook
python hooks/test_task_completed.py
```

Logs are written to `hook.log` in the repo root.
