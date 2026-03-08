<!--
 * @Author: qiangqiang.luan qiangqiang.luan@17zuoye.com
 * @Date: 2026-03-07 11:17:31
 * @LastEditors: qiangqiang.luan qiangqiang.luan@17zuoye.com
 * @LastEditTime: 2026-03-07 11:17:47
 * @FilePath: /article-video-to-social/references/workflow.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# 文章/视频 → 社交媒体工作流

## 目标
将 B 站视频或微信公众号文章转为文字，提炼核心观点，深度挖掘对投资的启示，最终通过 social-push 发布到社交媒体。

## 前置条件
- 已安装：`yt-dlp`、`ffmpeg`
- 已创建 faster-whisper 虚拟环境：`$OPENCLAW_WORKSPACE/.venv_faster_whisper`（默认路径 `~/.openclaw/workspace`，使用 medium 模型）
- 已配置 [social-push](https://github.com/aluan/social-push) 工具

## 步骤

### A. 获取原始内容

#### A1. B站视频转写
1. 运行脚本：
   ```bash
   python3 scripts/transcribe_bili_tiny.py <BV_ID或URL> /tmp/transcript.txt
   ```
   脚本会优先尝试下载B站字幕（含自动生成字幕），获取不到字幕时自动回退到 faster-whisper 语音转写。
2. 打开转写文件，修正明显识别错误（口误、重复、错字）。

#### A2. 微信公众号文章提取
1. 有链接时的处理流程：
   - 第一步：打开并等待加载：
     ```bash
     agent-browser open <URL>
     agent-browser wait --load networkidle
     ```
   - 第二步：获取标题和正文（用 `#js_content` 定位微信正文容器，避免抓到全页 UI 噪音）：
     ```bash
     agent-browser get title
     agent-browser snapshot -s "#js_content" > /tmp/article.txt
     ```
   - 第三步：若 `#js_content` 为空（少数模板不同），降级用：
     ```bash
     agent-browser snapshot -s ".rich_media_content" > /tmp/article.txt
     ```
   - 第四步：若仍不完整，提示用户复制粘贴
2. 无链接时让用户直接粘贴全文或关键段落。
3. 清理格式：去掉广告、版权声明、二维码等非正文内容（snapshot 输出的是 a11y 文本树，图片会显示为 `img "图片"`，可忽略）。

### B. 核心观点提炼
1. 用"要点清单"提炼 5-8 条核心观点。
2. 对每条观点进行深度解读和二次表达。
3. 形成 1-2 句核心金句。

### C. 投资启示分析

用 2-3 句话提炼对投资的深度启示：
- 聚焦投资理念、市场洞察或风险认知中的一个核心点
- 避免泛泛而谈，要有具体的洞察
- 保持简洁有力，不超过 3 句话

**详细指导**：参考 `assets/rewrite_prompt.md` 中的"投资启示分析"部分

### D. 发布到社交媒体
1. 使用 [social-push](https://github.com/aluan/social-push) 发布
2. 发布前向用户确认：
   - 内容是否符合预期
   - 投资启示是否有深度
   - 目标平台选择
   - 发布时间安排
3. 根据 social-push 配置完成发布

## 内容质量标准
- 核心观点清晰且有深度
- 投资启示简洁有力（2-3句话），有具体洞察
- 避免表面化和泛泛而谈
- 逻辑严密，论证充分

## 验证点
- 内容已完成核心观点提炼和投资启示分析
- 符合目标平台的内容规范和格式要求
- 用户已确认内容质量和发布计划
- 通过 social-push 成功发布
