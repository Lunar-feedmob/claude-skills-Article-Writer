
# Article Writer Skill - 使用说明

深度科普文章创作助手，从PDF文档到精美文章的完整解决方案。

## 功能特性

✨ **完整工作流程**（8步）
- Step 0: 智能PDF管理
- Step 1: 提取PDF文本
- Step 5: 提前提取图表
- Step 2: 生成深度解读
- Step 5.5: 生成纽约客风格插图（MCP nano-banana）
- Step 6: 撰写文章（初稿）
- **Step 6.5: 排版优化**（新增）- 移除emoji、优化图片位置、确保PDF质量
- Step 7: 最终输出（Markdown + PDF）
- Step 8: 完整交付报告

🎨 **特色功能**
- 可定制字数（4000-12000字）
- 独立封面图生成
- 中文优先+中文标点
- 口语化科普风格
- 丰富类比解释
- 纽约客插图风格

## 快速开始

### 1. 安装依赖

```bash
cd .claude/skills/article-writer/scripts
pip install -r requirements.txt
```

### 2. 配置MCP nano-banana

确保MCP配置文件包含nano-banana配置：

```json
{
  "nano-banana": {
    "command": "npx",
    "args": ["-y", "mcp-server-nano-banana"],
    "env": {
      "DUOMI_API_TOKEN": "YOUR_DUOMI_API_TOKEN_HERE"
    },
    "disabled": false,
    "autoApprove": ["generate_image"]
  }
}
```

### 3. 使用Skills

对Claude说：

```
用article-writer处理这个PDF，写一篇6000-8000字的文章
文件：./paper.pdf
```

或单独生成封面图：

```
用article-writer生成一张封面图
主题：人工智能的未来
```

## 详细使用

### 完整工作流

```
用户：帮我处理这个PDF文档
      文件路径：./research.pdf
      字数：6000-8000字

Claude会执行：
1. 验证PDF文件
2. 提取文本和图表
3. 生成深度分析
4. 确认创作方向
5. 生成纽约客风格插图
6. 撰写文章（口语化科普风格）
7. 导出MD和PDF格式
8. 提供完整交付报告
```

### 单独生成封面图

```
用户：我需要一张文章封面图
      主题：量子计算的突破
      风格：科技感

Claude会：
1. 设计视觉方案
2. 用MCP nano-banana生成图片
3. 保存为16:9高清图片
4. 可选：生成多个版本供选择
```

## 输出文件结构

```
article_output/
├── final_article.md          # Markdown格式文章
├── final_article.pdf         # PDF格式文章
├── analysis/
│   └── deep_analysis.md      # 深度解读分析
├── images/                   # 纽约客风格插图
│   ├── 01_cover_illustration.png
│   ├── 02_section1_illustration.png
│   └── ...
├── charts/                   # 原始PDF图表
│   └── ...
└── text/
    └── extracted_text.txt    # 提取的文本
```

## 脚本工具

### extract_text.py - 文本提取

```bash
python scripts/extract_text.py input.pdf output.txt
```

### extract_charts.py - 图表提取

```
bash
python scripts/extract_charts.py input.pdf output_dir/
```

### generate_pdf.py - PDF生成

```bash
python scripts/generate_pdf.py \
  article.md \
  article.pdf \
  --images-dir images/ \
  --font "Source Han Sans SC"
```

### count_words.py - 字数统计

```bash
python scripts/count_words.py article.md
```

### remove_emoji.py - Emoji移除工具 **（新增）**

```bash
# 检查和移除emoji字符（避免PDF乱码）
python scripts/remove_emoji.py article.md

# 或指定输出文件
python scripts/remove_emoji.py article.md clean_article.md
```

功能：
- 自动检测emoji字符
- 移除所有emoji和特殊符号
- 备份原文件（.bak）
- 统计移除数量

## 排版优化（Step 6.5）

### 问题诊断和解决

**问题1：PDF中文显示为方块**

```bash
# 诊断
fc-list :lang=zh-cn

# 解决
sudo apt-get install -y fonts-noto-cjk fonts-noto-cjk-extra
fc-cache -fv
```

**问题2：Emoji显示为乱码**

```bash
# 自动移除emoji
python scripts/remove_emoji.py article_output/final_article.md
```

**问题3：图片周围有大片留白**

- 将图片从章节开头移到段落之后
- 确保图片前有2-3段文字（200-300字）
- 使用工具检查：
  ```bash
  grep -B 3 "!\[\]" article.md | grep "^##"
  ```

**详细故障排除**：参见 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## 文章风格特点

### 口语化表达

✅ **使用**：
- "咱们来看看..."
- "简单来说..."
- "打个比方..."
- "你可以这样理解..."

❌ **避免**：
- 生硬的学术用语
- 复杂的长句
- 罕见的书面词汇

### 丰富类比

每个复杂概念都配有日常生活类比：

```
概念：轨道共振

简单来说：两个天体运行周期的整数比关系。

打个比方：这就像两个朋友散步，一个快一个慢，
但快的人每走3圈，慢的人正好走2圈，他们会定期相遇。

科学解释：在天体力学中...
```

### 中文标点

全文使用中文标点符号：，。！？：；""''

## 纽约客插图风格

所有插图特点：
- ✏️ 简洁线条艺术
- 🎨 2-3种颜色
- 💡 聪明的视觉隐喻
- 😊 略带幽默或思考性
- 📐 干净的构图

生成方式：MCP nano-banana

## 字数控制

用户可选择：
- 精华版：4000-6000字（10-15分钟阅读）
- 标准版：6000-8000字（15-20分钟阅读）
- 深度版：8000-12000字（25-30分钟阅读）
- 自定义：用户指定字数

## 常见问题

### Q: 如何安装中文字体？

A: 推荐使用思源黑体（Source Han Sans SC）或思源宋体（Noto Serif SC）。

macOS:
```bash
brew install --cask font-source-han-sans
```

Ubuntu/Debian:
```bash
sudo apt install fonts-noto-cjk
```

### Q: PDF生成失败怎么办？

A: 确保安装了所有依赖：

```bash
pip install --upgrade markdown2 weasyprint Pillow
```

如果是字体问题，使用系统已安装的中文字体。

### Q: 图片生成失败？

A: 检查MCP nano-banana配置：
1. API Token是否有效
2. 网络连接是否正常
3. MCP服务是否正常运行

### Q: 如何调整文章风格？

A: 在确认创作方向时（Step 2之后），告诉Claude：
```
请调整风格为更正式/更轻松/更专业...
```

## 技术要求

- Python 3.8+
- MCP nano-banana配置
- 网络连接（图片生成）
- 中文字体（PDF生成）

## 文件说明

- `SKILL.md` - Skills核心定义
- `scripts/` - Python工具脚本
  - `extract_text.py` - PDF文本提取
  - `extract_charts.py` - 图表提取
  - `generate_pdf.py` - PDF生成
  - `count_words.py` - 字数统计
  - `requirements.txt` - 依赖列表
- `README.md` - 本文档

## 更新日志

### v1.0.0 (2026-01-08)

- ✅ 完整的7步工作流程
- ✅ MCP nano-banana图片生成
- ✅ 中文优先+中文标点
- ✅ 口语化科普风格
- ✅ 可定制字数
- ✅ 独立封面图生成
- ✅ Markdown和PDF双格式导出

## 许可

MIT License

## 支持

如有问题，请在GitHub Issues中提出。

---

Happy Writing! 📝✨
