# Cursed Claude Code Hooks

A collection of Claude Code hooks that do things you probably shouldn't do.

## Hooks

### `hooks/user_prompt_submit.py` — Prompt roaster

A `UserPromptSubmit` hook that intercepts every prompt you send to Claude Code, calls an LLM to generate a sharp/critical remark about it, and reads it aloud via TTS.

### `hooks/stop.py` — Task complete quip

A `Stop` hook that fires when Claude finishes responding, generating a dry sardonic one-liner and reading it aloud.

### `hooks/task_completed.py` — Task done quip

A `TaskCompleted` hook that fires when a task is marked as complete, generating a sardonic remark about finishing work and reading it aloud.

Both hooks use [pocket-tts](https://github.com/kyutai-labs/pocket-tts) for high-quality local TTS, with macOS `say` as a fallback.

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

### 3. Register the hooks in `~/.claude/settings.json`

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/cursed-claude-code/hooks/user_prompt_submit.py"
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
            "command": "/path/to/cursed-claude-code/hooks/stop.py"
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
            "command": "/path/to/cursed-claude-code/hooks/task_completed.py"
          }
        ]
      }
    ]
  }
}
```

Replace `/path/to/cursed-claude-code` with the actual path to this repo.

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
python hooks/test_hook.py
python hooks/test_hook.py "your prompt here"

# Test the Stop hook
python hooks/test_stop.py

# Test the TaskCompleted hook
python hooks/test_task_completed.py
```

Logs are written to `hook.log` in the repo root.
