# xhs-bili-to-xhs

将 B 站视频转写为文字，进行总结提炼与爆款风格重写，并通过浏览器自动化写入小红书长文草稿（不自动发布）。

## 功能概览
- 支持 B 站 BV 号或链接转写（faster-whisper tiny）
- 自动“脱水总结 + 爆款风格重写”
- 写入小红书长文草稿（仅暂存，不点击发布）

## 环境准备
1) 安装依赖
```bash
brew install yt-dlp ffmpeg
```

2) 创建 faster-whisper 虚拟环境
```bash
python3 -m venv /Users/aluan/.openclaw/workspace/.venv_faster_whisper
source /Users/aluan/.openclaw/workspace/.venv_faster_whisper/bin/activate
pip install --upgrade pip
pip install faster-whisper
```

## 使用示例
### 1. 转写 B 站视频
```bash
python3 skills/xhs-bili-to-xhs/scripts/transcribe_bili_tiny.py BV1xxxxxxx /Users/aluan/.openclaw/workspace/tmp/bili_transcript.txt
```
或使用链接：
```bash
python3 skills/xhs-bili-to-xhs/scripts/transcribe_bili_tiny.py "https://www.bilibili.com/video/BV1xxxxxxx" /Users/aluan/.openclaw/workspace/tmp/bili_transcript.txt
```

### 2. 按爆款模版重写
参考：`assets/xhs_template.txt` 与 `references/workflow.md`

### 3. 写入小红书长文草稿
进入创作平台：
```
https://creator.xiaohongshu.com/publish/publish?source=official&from=tab_switch&target=article
```
按模板填写标题与正文 → 一键排版 → 暂存离开。

## 注意事项
- 本工具**不会自动点击发布**。
- 如遇 B 站高码率限制，可使用登录 cookie 或更换网络。
- 识别文本可能有误差，建议人工快速校对。

## 安装为 Skill
- 直接使用本目录，或安装 `dist/` 下的 `.skill` 包。
