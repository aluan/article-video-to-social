---
name: xhs-bili-to-xhs
description: Convert a Bilibili video link (BV or URL) into a tiny-model transcript and publish it to Xiaohongshu as a long-article draft using browser automation. Use when the user asks to transcribe a Bilibili video and post the text to Xiaohongshu (especially “B站转写/发小红书/草稿” workflows).
---

# B站转写 → 小红书长文草稿

## Overview
将 B 站视频转写为文字 → 总结提炼 → 按小红书爆款风格重写 → 写入小红书长文草稿（禁止自动发布）。

## Workflow (follow in order)

1. **转写文本**
   - 运行脚本：
     ```bash
     python3 skills/xhs-bili-to-xhs/scripts/transcribe_bili_tiny.py <BV_ID或URL> /Users/aluan/.openclaw/workspace/tmp/bili_transcript.txt
     ```
   - 打开转写文件，必要时修正明显识别错误与标题。

2. **总结与重写**
   - 先“脱水总结”，再按小红书爆款模板重写。
   - 模板见：`references/workflow.md` 和 `assets/xhs_template.txt`。

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
- `scripts/transcribe_bili_tiny.py`：使用 faster-whisper tiny 转写
- `assets/xhs_template.txt`：小红书爆款长文模板
