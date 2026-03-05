# xhs-bili-to-xhs

A skill to transcribe Bilibili videos with faster-whisper (tiny), summarize and rewrite into Xiaohongshu “爆款” long-article drafts, and save them as Xiaohongshu drafts via browser automation.

## What it does
- Transcribe Bilibili videos from BV or URL
- Summarize + rewrite into Xiaohongshu爆款风格
- Save as Xiaohongshu long-article drafts (no auto publish)

## Usage (OpenClaw)
- Use the skill folder directly, or install the packaged `.skill` file from `dist/`.

## Notes
- Requires `yt-dlp`, `ffmpeg`, and a local `faster-whisper` venv at `.venv_faster_whisper`.
- Will not click “发布” automatically.
