# article-video-to-social

将网页文章和视频内容转换为适合社交媒体的格式，并通过 [social-push-skill](https://github.com/aluan/social-push-skill) 发送到各大社交平台。

## 功能概览
- **视频转文字**：支持 B 站视频（BV 号或链接）转写（faster-whisper medium）
- **文章提取**：支持微信公众号文章正文提取（链接抓取或手动粘贴）
- **智能改写**：自动总结提炼 + 社交媒体风格重写
- **多平台发布**：通过 social-push-skill 发送到各大社交平台

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

## 使用流程

### 1. 获取内容源
**B 站视频转写**
```bash
python3 "$OPENCLAW_WORKSPACE/skills/article-video-to-social/scripts/transcribe_bili_tiny.py" BV1xxxxxxx /path/to/output.txt
```
或使用完整链接：
```bash
python3 "$OPENCLAW_WORKSPACE/skills/article-video-to-social/scripts/transcribe_bili_tiny.py" "https://www.bilibili.com/video/BV1xxxxxxx" /path/to/output.txt
```

**微信公众号文章提取**
- 有链接：优先使用 `web_fetch` 抓取正文，不完整则浏览器打开后复制
- 无链接：直接粘贴全文或关键段落
- 自动清理广告、版权声明、二维码等非正文内容

### 2. 内容处理
- 核心观点提炼：提取 5-8 条核心观点
- 投资启示分析：深度挖掘对投资的启示
- 格式优化：适配社交媒体展示格式

### 3. 发布到社交平台
通过 [social-push-skill](https://github.com/aluan/social-push-skill) 发送到目标平台：
- 小红书
- 微博
- 微信公众号
- 其他社交平台（根据 social-push-skill 支持情况）

## 注意事项
- 视频转写可能有误差，建议人工快速校对
- 如遇 B 站高码率限制，可使用登录 cookie 或更换网络
- 发布前请确认内容符合各平台规范
- 发布操作由 social-push-skill 处理，具体配置请参考其文档

## 相关资源
- [social-push-skill](https://github.com/aluan/social-push-skill) - 社交媒体发布工具
- `assets/rewrite_prompt.md` - 专业洗稿重写提示词
- `references/workflow.md` - 详细工作流程

## 安装为 Skill
直接使用本目录，或安装 `dist/` 下的 `.skill` 包。
