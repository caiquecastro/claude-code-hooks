# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Cursed Hooks — a collection of hooks for Claude Code and Codex that intercept workflow events (prompt submission, response completion, task completion), generate snarky commentary via an LLM (OpenRouter), and play it aloud via text-to-speech. Both tools share the same hook format.

## Commands

```sh
# Install dependencies
uv sync

# Test individual hooks
python hooks/test_user_prompt_submit.py ["optional prompt"]
python hooks/test_stop.py
python hooks/test_task_completed.py
```

There is no formal test suite or linter configured. The test scripts simulate Claude Code hook invocations by piping JSON payloads to the hook scripts.

## Architecture

All hooks live in `hooks/` and share a common pattern:
1. Read JSON payload from stdin
2. Check `is_enabled()` — controlled by `HOOKS_ENABLED` env var
3. Call `detach()` to fork (parent exits immediately so Claude Code isn't blocked)
4. Generate a remark via OpenRouter LLM
5. Speak it aloud via `speak()` (pocket-tts with macOS `say` fallback)

**`hooks/shared.py`** is the central module containing all shared logic: LLM client setup, TTS (with fallback), personality system (5 personalities chosen randomly per invocation), logging, and the `detach()` fork mechanism.

Each hook script (e.g., `user_prompt_submit.py`) uses a `#!/usr/bin/env -S uv run` shebang with PEP 723 inline dependency declarations, so `uv` resolves dependencies automatically without a virtualenv.

## Key Configuration

- **LLM model**: `MODEL` constant in `shared.py` (default: `anthropic/claude-haiku-4-5` via OpenRouter)
- **TTS voice**: `VOICE` constant in `shared.py` (default: `alba`)
- **API key**: `OPENROUTER_API_KEY` in `.env`
- **Enable/disable**: Set `HOOKS_ENABLED=false` in environment to disable all hooks

## Requirements

- macOS (TTS fallback uses `say`)
- `uv` package manager
- OpenRouter API key
