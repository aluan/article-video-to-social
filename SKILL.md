<!--
Source Code Repositories:
- wenyan: https://github.com/aluan/wenyan
- xhs (xiaohongshu-cli): https://github.com/aluan/xiaohongshu-cli
- xhs-textcard: https://github.com/aluan/XHS-TextCard
-->
---
name: article-video-to-social
description: Convert Bilibili videos or WeChat articles into social media content. Transcribe videos, extract article text, summarize and rewrite in platform-specific style, then publish to WeChat (wenyan) and Xiaohongshu (xhs). Use when user asks to convert B站视频/公众号文章 to social media posts.
license: MIT
metadata:
  author: aluan
  version: 1.0.3
  requires:
    - bili
    - pandoc
    - wenyan
    - xhs-textcard
    - xhs
---

# 文章视频转社交媒体

## Overview
将 B 站视频或微信公众号文章转为文字 → 总结提炼 → 按目标平台风格重写 → 发布到微信公众号（wenyan）和小红书（xhs）。

## Progress Feedback（进度反馈规则）

每个步骤完成后，必须立即向用户输出对应的进度反馈，格式如下：

| 步骤完成事件 | 反馈消息 |
|---|---|
| 公众号文章获取完毕 | `✅ 公众号文章获取成功` |
| B站视频转写完毕 | `✅ 视频内容转写成功` |
| 洗稿重写完毕 | `✅ 洗稿成功` |
| 发布到小红书完毕 | `✅ 发布到小红书成功` |
| 发布到微信公众号完毕 | `✅ 发布到微信公众号成功` |

若步骤失败，输出 `❌ <步骤名> 失败：<简短原因>`，然后尝试降级方案或提示用户。

---

## Workflow (follow in order)

0. **Pre-flight：清理残留进程**（每次 workflow 开始前必做）
   ```bash
   agent-browser close 2>/dev/null || true
   ```
   此步骤确保上一次 agent-browser 进程已退出，避免出现 `Target page ... closed` 或 `--profile ignored` 报错。
   静默执行，无需向用户反馈。

1. **获取原始内容**
   - **B站视频**：
     - 先告知用户：`⏳ 正在获取视频字幕，请稍候...`
     - 使用 bili 命令下载字幕：
       ```bash
       bili video <BV_ID> --subtitle > /tmp/transcript.txt 2>&1
       ```
     - 如果命令成功（退出码为 0）且 `/tmp/transcript.txt` 有内容，则字幕下载成功
     - 如果字幕下载失败，提示用户该视频没有可用字幕
     - 字幕获取成功后，打开文件检查并修正明显识别错误
     - **完成后输出**：`✅ 视频内容转写成功`

   - **微信公众号文章**：
     - 有链接：
       1. 先告知用户：`⏳ 正在打开页面，请稍候...`
       2. 打开并等待加载：
          ```bash
          agent-browser open <URL>
          agent-browser wait --load networkidle
          ```
       3. 获取标题和正文（用 `#js_content` 定位微信正文容器，避免抓到全页 UI 噪音）：
          ```bash
          agent-browser get title
          agent-browser snapshot -s "#js_content" > /tmp/article.txt
          ```
       4. 若 `#js_content` 为空（少数模板不同），降级用：
          ```bash
          agent-browser snapshot -s ".rich_media_content" > /tmp/article.txt
          ```
       5. 若仍不完整，提示用户复制粘贴
     - 无链接：让用户直接粘贴全文或关键段落
     - 清理广告、版权声明、二维码等非正文内容（snapshot 输出的是 a11y 文本树，图片会显示为 `img "图片"`，可忽略）
     - **完成后输出**：`✅ 公众号文章获取成功`

2. **内容处理**
   - **洗稿重写**：参考 `assets/rewrite_prompt.md` 进行专业的内容重写
   - **格式优化**：根据目标平台调整展示格式
   - **完成后输出**：`✅ 洗稿成功`

3. **发布到社交平台**
   - 支持平台：微信公众号（wenyan）、小红书（xhs）
   - 发布前向用户确认内容
   - 用户确认后，如果用户没有指定发布平台，默认就发布到支持的所有平台（微信公众号、小红书），如果用户指定了发布平台，就只发布到指定的平台。

   **发布流程**（按顺序执行）：
   - **微信公众号**：
     - 使用 `wenyan --theme Maize` 命令发布
     - 发布后输出：`✅ 发布到微信公众号成功` 或 `❌ 发布到微信公众号失败：<简短原因>`
   - **小红书**：
     - 使用 `xhs-textcard -i` 命令生成卡片图片
     - 使用 `xhs` 命令发布笔记
     - 发布后输出：`✅ 发布到小红书成功` 或 `❌ 发布到小红书失败：<简短原因>`

## Rules

### 内容处理规则
- 避免大段原文照搬，必须重组与提炼
- 保留原文核心观点，深度挖掘投资价值
- 用"要点清单"提炼 5-8 条核心观点
- 对每条观点进行深度解读和二次表达
- 形成 1-2 句核心金句

### 投资启示分析
- 用 2-3 句话提炼对投资的深度启示
- 聚焦投资理念、市场洞察或风险认知中的一个核心点
- 避免泛泛而谈，要有具体的洞察
- 保持简洁有力，不超过 3 句话

### 内容质量标准
- 核心观点清晰且有深度
- 投资启示简洁有力（2-3句话），有具体洞察
- 避免表面化和泛泛而谈
- 逻辑严密，论证充分

### 发布规范
- 尊重各平台内容规范，避免敏感词和违规内容
- 出现违禁词语时的处理方式：直接停止发布，同时提示用户内容可能违规
- 发布前必须向用户确认内容质量和发布计划
- 确保符合目标平台的内容规范和格式要求

## References
- 发布工具：`wenyan`（微信公众号）、`xhs`（小红书）

## Resources
- `assets/rewrite_prompt.md`：专业的洗稿重写提示词
