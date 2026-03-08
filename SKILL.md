---
name: article-video-to-social
description: Convert Bilibili videos or WeChat articles into social media content. Transcribe videos, extract article text, summarize and rewrite in platform-specific style, then publish via social-push. Use when user asks to convert B站视频/公众号文章 to social media posts.
---

# 文章视频转社交媒体

## Overview
将 B 站视频或微信公众号文章转为文字 → 总结提炼 → 按目标平台风格重写 → 通过 social-push 发布到社交媒体。

## Workflow (follow in order)

1. **获取原始内容**
   - **B站视频**：
     ```bash
     python3 scripts/transcribe_bili_tiny.py <BV_ID或URL> /tmp/transcript.txt
     ```
     脚本会优先尝试下载B站字幕（含自动生成字幕），获取不到字幕时自动回退到 faster-whisper 语音转写。
     转写完成后，打开文件检查并修正明显识别错误。

   - **微信公众号文章**：
     - 有链接：
       1. 打开并等待加载：
          ```bash
          agent-browser open <URL>
          agent-browser wait --load networkidle
          ```
       2. 获取标题和正文（用 `#js_content` 定位微信正文容器，避免抓到全页 UI 噪音）：
          ```bash
          agent-browser get title
          agent-browser snapshot -s "#js_content" > /tmp/article.txt
          ```
       3. 若 `#js_content` 为空（少数模板不同），降级用：
          ```bash
          agent-browser snapshot -s ".rich_media_content" > /tmp/article.txt
          ```
       4. 若仍不完整，提示用户复制粘贴
     - 无链接：让用户直接粘贴全文或关键段落
     - 清理广告、版权声明、二维码等非正文内容（snapshot 输出的是 a11y 文本树，图片会显示为 `img "图片"`，可忽略）

2. **内容处理**
   - **洗稿重写**：参考 `assets/rewrite_prompt.md` 进行专业的内容重写
   - **格式优化**：根据目标平台调整展示格式

3. **发布到社交平台**
   - 使用 [social-push](https://github.com/aluan/social-push) 发布
   - 支持平台：小红书、微博、微信公众号等（根据 social-push 配置）
   - 发布前向用户确认内容和目标平台

## Rules
- 避免大段原文照搬，必须重组与提炼
- 发布前必须向用户确认内容和目标平台
- 尊重各平台内容规范和字数限制
- 保留原文核心观点，深度挖掘投资价值

## References
- 详细流程：`references/workflow.md`
- 发布工具：[social-push](https://github.com/aluan/social-push)

## Resources
- `scripts/transcribe_bili_tiny.py`：使用 faster-whisper medium 转写 B 站视频
- `assets/rewrite_prompt.md`：专业的洗稿重写提示词
- `references/workflow.md`：详细工作流程说明
