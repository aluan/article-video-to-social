#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys
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

    workspace = Path("/Users/aluan/.openclaw/workspace")
    venv_python = workspace / ".venv_faster_whisper" / "bin" / "python"
    if not venv_python.exists():
        print("Error: faster-whisper venv not found at .venv_faster_whisper. Create it first.")
        sys.exit(1)

    tmp_dir = workspace / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    audio_path = tmp_dir / f"{bv_id}_audio.mp3"

    url = source if source.startswith("http") else f"https://www.bilibili.com/video/{bv_id}"

    run([
        "yt-dlp",
        "-x",
        "--audio-format",
        "mp3",
        "-o",
        str(audio_path),
        url,
    ])

    script = (
        "from faster_whisper import WhisperModel\n"
        "model = WhisperModel('tiny', device='cpu', compute_type='int8')\n"
        f"segments, info = model.transcribe('{audio_path}', language='zh')\n"
        "text = ''.join(seg.text for seg in segments)\n"
        f"open('{output_txt}','w',encoding='utf-8').write(text.strip())\n"
    )
    run([str(venv_python), "-c", script])
    print(f"OK: transcript written to {output_txt}")


if __name__ == "__main__":
    main()
