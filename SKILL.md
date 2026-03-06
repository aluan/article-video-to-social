---
name: xhs-bili-to-xhs
description: Convert a Bilibili video link (BV or URL) or a WeChat public-article into text, summarize and rewrite it, then publish it to Xiaohongshu as a long-article draft using browser automation. Use when the user asks to transcribe B站 or改写公众号文章发小红书（草稿）。
---

# B站/公众号文章 → 小红书长文草稿

## Overview
将 B 站视频或公众号文章转为文字 → 总结提炼 → 按小红书爆款风格重写 → 写入小红书长文草稿（禁止自动发布）。

## Workflow (follow in order)

1. **获取原文（B站/公众号）**
   - B站：
     ```bash
     python3 skills/xhs-bili-to-xhs/scripts/transcribe_bili_tiny.py <BV_ID或URL> /Users/aluan/.openclaw/workspace/tmp/bili_transcript.txt
     ```
     打开转写文件，必要时修正明显识别错误与标题。
   - 公众号：
     - 有链接时用 `web_fetch` 抓正文，抓取不完整则用浏览器打开后复制正文。
     - 无链接时让用户直接粘贴全文或关键段落。
     - 清理广告、版权声明、二维码等非正文内容。

2. **总结与重写**
   - 先“脱水总结”，再按小红书爆款模板重写。
   - 模板见：`references/workflow.md` 和 `assets/xhs_template.md`。

3. **确认登录**
   - 若未登录：打开 `https://www.xiaohongshu.com/` 获取二维码截图，发送给用户扫码。
   - 登录成功后，页面顶部应显示“我”。

4. **写入小红书长文草稿**
   - 打开：`https://creator.xiaohongshu.com/publish/publish?source=official&from=tab_switch&target=article`
   - 点击“新的创作”，填写标题与正文内容（用重写后的版本）。
   - 点击“一键排版”。
   - 点击“暂存离开”。

## Rules
- **禁止自动点击“发布”**，只能保存草稿。
- 每个关键步骤后用 `agent-browser snapshot -i` 复核页面元素。
- 避免大段原文照搬，必须重组与提炼。

## References
- 详细流程见：`references/workflow.md`

## Resources
- `scripts/transcribe_bili_tiny.py`：使用 faster-whisper medium 转写
- `assets/xhs_template.md`：小红书爆款长文模板
- `references/workflow.md`：公众号文章处理细则
