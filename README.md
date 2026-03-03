# Cursed Claude Code Hooks

A collection of Claude Code hooks that do things you probably shouldn't do.

## Hooks

### `user_prompt_submit.py` — TTS prompt reader

A `UserPromptSubmit` hook that speaks your prompt out loud using macOS's built-in `say` command every time you submit a message to Claude Code.

**Requirements:** macOS (uses the `say` command)

## Setup

Register the hook in your Claude Code settings (`~/.claude/settings.json`):

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/cursed-claude-code/user_prompt_submit.py"
          }
        ]
      }
    ]
  }
}
```

Replace `/path/to/cursed-claude-code` with the actual path to this repo.
