#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys
import glob
from pathlib import Path


def usage():
    print("Usage: transcribe_bili_tiny.py <BV_ID or bilibili url> <output_txt>")


def extract_bv_id(value: str) -> str:
    if value.startswith("BV"):
        return value
    match = re.search(r"BV[0-9A-Za-z]{10}", value)
    if match:
        return match.group(0)
    return ""


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def parse_vtt(vtt_path: str) -> str:
    """Parse VTT subtitle file, return plain text without timestamps."""
    with open(vtt_path, encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    texts = []
    seen = set()
    for line in lines:
        line = line.strip()
        # Skip header, blank lines, timestamps, and NOTE lines
        if not line or line == "WEBVTT" or line.startswith("NOTE") or "-->" in line:
            continue
        # Skip numeric cue identifiers
        if re.match(r"^\d+$", line):
            continue
        # Remove HTML tags
        line = re.sub(r"<[^>]+>", "", line)
        if line and line not in seen:
            seen.add(line)
            texts.append(line)

    return "\n".join(texts)


def try_download_subtitle(url: str, bv_id: str, tmp_dir: Path) -> str | None:
    """
    Try downloading subtitles via yt-dlp.
    Returns the subtitle text if successful, None otherwise.
    """
    subtitle_base = tmp_dir / f"{bv_id}_sub"
    # Remove any previous subtitle files
    for f in glob.glob(str(subtitle_base) + ".*"):
        os.remove(f)

    try:
        subprocess.run(
            [
                "yt-dlp",
                "--write-sub",
                "--write-auto-sub",
                "--sub-langs", "zh,zh-Hans,zh-CN,zh-TW,en",
                "--skip-download",
                "-o", str(subtitle_base),
                url,
            ],
            capture_output=True,
            text=True,
        )
    except Exception as e:
        print(f"yt-dlp subtitle download failed: {e}")
        return None

    # Find downloaded subtitle files (.vtt preferred)
    vtt_files = glob.glob(str(subtitle_base) + "*.vtt")
    if not vtt_files:
        # Also check for .srt or other formats
        sub_files = glob.glob(str(subtitle_base) + ".*")
        sub_files = [f for f in sub_files if not f.endswith(".mp3")]
        if not sub_files:
            return None
        sub_file = sub_files[0]
        with open(sub_file, encoding="utf-8") as f:
            return f.read().strip()

    # Parse VTT
    vtt_file = vtt_files[0]
    text = parse_vtt(vtt_file)
    if text.strip():
        print(f"OK: subtitle downloaded from {vtt_file}")
        return text.strip()
    return None


def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    source = sys.argv[1]
    output_txt = Path(sys.argv[2]).expanduser().resolve()
    bv_id = extract_bv_id(source)
    if not bv_id:
        print("Error: Unable to extract BV id from input.")
        sys.exit(1)

    url = source if source.startswith("http") else f"https://www.bilibili.com/video/{bv_id}"

    workspace = Path(os.environ.get("OPENCLAW_WORKSPACE", "~/.openclaw/workspace")).expanduser()
    tmp_dir = workspace / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Try subtitle first
    print("Trying to download subtitles...")
    subtitle_text = try_download_subtitle(url, bv_id, tmp_dir)
    if subtitle_text:
        output_txt.write_text(subtitle_text, encoding="utf-8")
        print(f"OK: subtitle written to {output_txt}")
        return

    # Step 2: Fall back to whisper transcription
    print("No subtitles found, falling back to whisper transcription...")
    venv_python = workspace / ".venv_faster_whisper" / "bin" / "python"
    if not venv_python.exists():
        print("Error: faster-whisper venv not found at .venv_faster_whisper. Create it first.")
        sys.exit(1)

    audio_path = tmp_dir / f"{bv_id}_audio.mp3"
    run([
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "-o", str(audio_path),
        url,
    ])

    script = (
        "from faster_whisper import WhisperModel\n"
        "model = WhisperModel('medium', device='cpu', compute_type='int8')\n"
        f"segments, info = model.transcribe('{audio_path}', language='zh')\n"
        "text = ''.join(seg.text for seg in segments)\n"
        f"open('{output_txt}','w',encoding='utf-8').write(text.strip())\n"
    )
    run([str(venv_python), "-c", script])
    print(f"OK: transcript written to {output_txt}")


if __name__ == "__main__":
    main()
