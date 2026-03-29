# article-video-to-social

将 B 站视频和微信公众号文章转换为适合社交媒体的格式，并直接发布到微信公众号和小红书。

## 源码仓库
- [wenyan](https://github.com/aluan/wenyan) - 微信公众号发布工具
- [xiaohongshu-cli](https://github.com/aluan/xiaohongshu-cli) - 小红书发布工具
- [XHS-TextCard](https://github.com/aluan/XHS-TextCard) - 小红书卡片图片生成工具

## 功能概览
- **视频字幕提取**：支持 B 站视频字幕下载（BV 号或链接）
- **文章提取**：支持微信公众号文章正文提取（链接抓取或手动粘贴）
- **智能改写**：自动总结提炼 + 社交媒体风格重写
- **多平台发布**：直接发布到微信公众号（wenyan）和小红书（xhs）

## 环境准备
安装依赖工具：
```bash
# 安装 bili 命令（B站字幕下载）
npm install -g @aluan/bili-cli

# 安装 pandoc（文档格式转换）
brew install pandoc

# 安装 wenyan（微信公众号发布）
npm install -g wenyan

# 安装 xhs（小红书发布）
npm install -g @aluan/xiaohongshu-cli

# 安装 xhs-textcard（小红书卡片图片生成）
npm install -g xhs-textcard
```

## 使用流程

### 1. 获取内容源
**B 站视频字幕下载**
```bash
bili video <BV_ID> --subtitle > /tmp/transcript.txt
```
或使用完整链接：
```bash
bili video "https://www.bilibili.com/video/BV1xxxxxxx" --subtitle > /tmp/transcript.txt
```

**微信公众号文章提取**
- 有链接：使用 agent-browser 打开页面并提取正文
- 无链接：直接粘贴全文或关键段落
- 自动清理广告、版权声明、二维码等非正文内容

### 2. 内容处理
- **核心观点提炼**：提取 5-8 条核心观点
- **投资启示分析**：深度挖掘对投资的启示（2-3 句话）
- **格式优化**：适配社交媒体展示格式

### 3. 发布到社交平台
**微信公众号**
```bash
wenyan --theme Maize
```

**小红书**
```bash
# 生成卡片图片
xhs-textcard -i

# 发布笔记
xhs
```

## 内容质量标准
- 核心观点清晰且有深度
- 投资启示简洁有力（2-3句话），有具体洞察
- 避免表面化和泛泛而谈
- 逻辑严密，论证充分

## 注意事项
- 字幕提取可能有误差，建议人工快速校对
- 如遇 B 站字幕下载失败，提示用户该视频没有可用字幕
- 发布前请确认内容符合各平台规范
- 出现违禁词语时会直接停止发布

## 相关资源
- `assets/rewrite_prompt.md` - 专业洗稿重写提示词

## 安装为 Skill
直接使用本目录，或安装 `dist/` 下的 `.skill` 包。
