#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys
import glob
from pathlib import Path


def usage():
    print("用法: transcribe_bili_tiny.py <BV_ID 或 bilibili 链接> <输出文本文件>")


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
                "--cookies-from-browser", "chrome",
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
        print(f"yt-dlp 字幕下载失败: {e}")
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
        print(f"成功: 已从 {vtt_file} 下载字幕")
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
        print("错误: 无法从输入中提取 BV ID")
        sys.exit(1)

    url = source if source.startswith("http") else f"https://www.bilibili.com/video/{bv_id}"

    workspace = Path(os.environ.get("OPENCLAW_WORKSPACE", "~/.openclaw/workspace")).expanduser()
    tmp_dir = workspace / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Try subtitle first
    print(f"步骤 1: 正在尝试下载 {bv_id} 的字幕...")
    subtitle_text = try_download_subtitle(url, bv_id, tmp_dir)
    if subtitle_text:
        output_txt.write_text(subtitle_text, encoding="utf-8")
        print(f"✓ 字幕已写入 {output_txt}")
        return

    # Step 2: Fall back to whisper transcription
    print("✗ 未找到字幕")
    print("步骤 2: 使用 Whisper 进行语音转录...")
    venv_python = workspace / ".venv_faster_whisper" / "bin" / "python"
    if not venv_python.exists():
        print("错误: 未找到 faster-whisper 虚拟环境，请先创建 .venv_faster_whisper")
        sys.exit(1)

    audio_path = tmp_dir / f"{bv_id}_audio.mp3"
    print(f"正在从 {url} 下载音频...")
    run([
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "-o", str(audio_path),
        url,
    ])
    print(f"✓ 音频下载完成: {audio_path}")

    print("正在启动 faster-whisper 转录（可能需要几分钟）...")
    script = (
        "from faster_whisper import WhisperModel\n"
        "import sys\n"
        "print('正在加载 Whisper 模型...')\n"
        "model = WhisperModel('medium', device='cpu', compute_type='int8')\n"
        "print('模型加载完成，开始转录音频...')\n"
        f"segments, info = model.transcribe('{audio_path}', language='zh')\n"
        "print(f'检测到的语言: {{info.language}} (概率: {{info.language_probability:.2f}})')\n"
        "print('正在处理音频片段...')\n"
        "texts = []\n"
        "total_duration = info.duration\n"
        "for i, seg in enumerate(segments):\n"
        "    texts.append(seg.text)\n"
        "    progress = (seg.end / total_duration) * 100 if total_duration > 0 else 0\n"
        "    if i % 10 == 0:\n"
        "        print(f'进度: {progress:.1f}% ({seg.end:.1f}秒 / {total_duration:.1f}秒)', flush=True)\n"
        "text = ''.join(texts)\n"
        f"open('{output_txt}','w',encoding='utf-8').write(text.strip())\n"
        "print('转录完成！')\n"
    )
    run([str(venv_python), "-c", script])
    print(f"✓ 转录文本已写入 {output_txt}")


if __name__ == "__main__":
    main()
