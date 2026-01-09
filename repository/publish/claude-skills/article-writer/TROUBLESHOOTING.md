# Article Writer - 故障排除指南

本文档总结了使用article-writer skill过程中可能遇到的所有问题及其解决方案。

## 目录

- [PDF生成问题](#pdf生成问题)
  - [问题1：中文显示为方块（豆腐块）](#问题1中文显示为方块豆腐块)
  - [问题2：Emoji显示为乱码](#问题2emoji显示为乱码)
  - [问题3：图片周围有大片留白](#问题3图片周围有大片留白)
  - [问题4：页码显示不符合预期](#问题4页码显示不符合预期)
- [图片生成问题](#图片生成问题)
  - [问题5：MCP nano-banana连接失败](#问题5mcp-nano-banana连接失败)
  - [问题6：图片生成超时](#问题6图片生成超时)
- [字数控制问题](#字数控制问题)
  - [问题7：生成的文章字数超出范围](#问题7生成的文章字数超出范围)
- [依赖安装问题](#依赖安装问题)
  - [问题8：WeasyPrint安装失败](#问题8weasyprint安装失败)

---

## PDF生成问题

### 问题1：中文显示为方块（豆腐块）

**症状**：
- PDF中大量中文字符显示为 □□□ 方块
- 只有英文和数字显示正常

**原因**：
- 系统未安装中文字体
- 或者字体配置不正确

**诊断步骤**：

```bash
# 1. 检查系统中文字体
fc-list :lang=zh-cn

# 2. 如果输出为空或只有几个字体，说明缺少中文字体
```

**解决方案**：

```bash
# 方案1：安装Noto CJK字体（推荐）
sudo apt-get update
sudo apt-get install -y fonts-noto-cjk fonts-noto-cjk-extra

# 方案2：安装WenQuanYi字体（备选）
sudo apt-get install -y fonts-wqy-microhei fonts-wqy-zenhei

# 3. 刷新字体缓存
fc-cache -fv

# 4. 验证安装
fc-list :lang=zh-cn | grep -i "noto"
```

**验证修复**：

```bash
# 重新生成PDF
python .claude/skills/article-writer/scripts/generate_pdf.py \
  article_output/final_article.md \
  article_output/final_article.pdf \
  --images-dir article_output/images/ \
  --font-family "Noto Sans CJK SC" \
  --chinese-punctuation

# 检查PDF（用PDF阅读器打开查看中文是否正常）
```

---

### 问题2：Emoji显示为乱码

**症状**：
- PDF中出现 ☑ □ 等奇怪符号
- 或者emoji位置显示为空白方块

**原因**：
- Markdown文件中使用了emoji字符（如 ✅ 📊 🎯 等）
- WeasyPrint使用的字体不支持emoji渲染

**诊断步骤**：

```bash
# 检查是否有emoji字符
grep -P "[\x{1F300}-\x{1F9FF}\x{2600}-\x{26FF}]|[✅☑✓✔❌]" article_output/final_article.md
```

**解决方案**：

```bash
# 方案1：使用自动化脚本移除emoji
python .claude/skills/article-writer/scripts/remove_emoji.py \
  article_output/final_article.md

# 脚本会：
# - 自动备份原文件为 .bak
# - 移除所有emoji字符
# - 统计移除的emoji数量

# 方案2：手动替换
# 常见的emoji替换：
# ✅ **不可变日志** → **不可变日志**
# - ✓ 中文表达 → - 中文表达
# 📊 图表 → 图表
```

**常见emoji列表**：

| Emoji | 描述 | 建议替换 |
|-------|------|---------|
| ✅ ☑ ✓ ✔ | 勾选符号 | 直接删除或用"是"、"完成" |
| ❌ ✗ | 叉号 | 直接删除或用"否"、"未完成" |
| 📊 📈 📉 | 图表 | 删除或用文字"图表"、"趋势" |
| 🎨 🖼️ | 艺术/图片 | 删除或用"图片"、"插图" |
| 💡 🔍 | 想法/搜索 | 删除或用"提示"、"查找" |
| 🎯 🎭 | 目标/艺术 | 删除或用"目标"、"主题" |

**验证修复**：

```bash
# 1. 确认emoji已移除
python .claude/skills/article-writer/scripts/remove_emoji.py article_output/final_article.md
# 应该显示：找到 0 个emoji字符

# 2. 重新生成PDF
python .claude/skills/article-writer/scripts/generate_pdf.py \
  article_output/final_article.md \
  article_output/final_article.pdf \
  --images-dir article_output/images/ \
  --font-family "Noto Sans CJK SC"
```

---

### 问题3：图片周围有大片留白

**症状**：
- PDF某些页面几乎是空白的，只有一张小图
- 图片前后有大量空白空间
- 页面利用率低

**原因**：
- 图片放置在章节/小节开头
- CSS的`page-break-inside: avoid`导致强制分页
- 图片尺寸设置不合理

**诊断步骤**：

```bash
# 检查图片位置（查看图片前3行是否有标题）
grep -B 3 "!\[\]" article_output/final_article.md | grep "^##"

# 如果输出很多结果，说明很多图片紧跟在标题后面
```

**解决方案**：

**方案1：调整图片位置（推荐）**

将图片从章节开头移动到段落之后：

```markdown
# 错误示例 ❌
## 第一部分：问题背景

![](images/01_problem.png)

这是问题的详细描述...

# 正确示例 ✅
## 第一部分：问题背景

这是问题的详细描述，经过几段文字的铺垫后...

当前的问题主要体现在三个方面：第一...第二...第三...

通过深入分析，我们发现...

![](images/01_problem.png)
<p align="center"><i>问题示意图</i></p>

基于以上分析...
```

**关键原则**：
1. **图片前至少有2-3段文字**（约200-300字）
2. **图片应该"解释"前面的文字**，而不是"引出"后面的文字
3. **图片说明要简洁**（10字以内）

**方案2：优化CSS配置**

在`generate_pdf.py`中已经优化的配置：

```python
img {
    max-width: 85%;           # 不是100%，留出边距
    max-height: 400pt;        # 限制最大高度
    margin: 12pt auto;        # 适度边距
    page-break-before: avoid; # 避免图片前强制分页
    page-break-after: auto;   # 允许图片后自然分页
}
```

**批量检查工具**：

创建 `check_image_positions.sh`：

```bash
#!/bin/bash
# 检查所有图片位置

echo "检查图片位置..."
echo "==============="

# 查找所有紧跟在标题后的图片
grep -B 3 "!\[\]" "$1" | grep -B 3 "^##" | grep "!\[\]" -A 1 -B 3

echo ""
echo "如果上面有输出，说明有图片紧跟在标题后面，需要调整"
```

**验证修复**：

重新生成PDF后，检查：
- 每页是否都充分利用了空间
- 图片周围是否有合理的文字内容
- 没有"孤零零"的图片页面

---

### 问题4：页码显示不符合预期

**症状**：
- PDF底部显示页码，但不希望显示
- 或者页码格式不正确

**原因**：
- CSS中配置了`@page @bottom-center`规则

**解决方案**：

修改`generate_pdf.py`中的CSS：

```python
# 不显示页码（推荐用于在线阅读）
@page {
    size: A4;
    margin: 2cm 1.5cm;
    # 不设置 @bottom-center 就没有页码
}

# 显示页码（适合打印）
@page {
    size: A4;
    margin: 2cm 1.5cm;
    @bottom-center {
        content: counter(page);
        font-size: 9pt;
        color: #666;
    }
}
```

**验证修复**：

```bash
# 重新生成PDF
python .claude/skills/article-writer/scripts/generate_pdf.py \
  article_output/final_article.md \
  article_output/final_article.pdf \
  --images-dir article_output/images/ \
  --font-family "Noto Sans CJK SC"

# 用PDF阅读器检查页码
```

---

## 图片生成问题

### 问题5：MCP nano-banana连接失败

**症状**：
- 调用图片生成时报错
- 提示MCP服务不可用

**原因**：
- MCP配置不正确
- API token无效或未设置

**诊断步骤**：

1. 检查MCP配置文件（通常在`~/.claude/mcp_settings.json`）

2. 验证nano-banana配置：

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

**解决方案**：

```bash
# 1. 检查npm和npx是否可用
npx --version

# 2. 测试nano-banana服务
npx -y mcp-server-nano-banana

# 3. 确认API token有效
# 联系DUOMI API获取有效token

# 4. 重启Claude Code
```

---

### 问题6：图片生成超时

**症状**：
- 图片生成等待很久
- 最终超时失败

**原因**：
- 网络连接问题
- API服务繁忙
- prompt过于复杂

**解决方案**：

```bash
# 方案1：增加超时时间
# 在调用generate_image时设置更长的超时
max_attempts: 120  # 从60增加到120

# 方案2：简化prompt
# 将复杂的prompt拆分为多个简单的prompt

# 方案3：重试机制
# 如果失败，等待几分钟后重试
```

---

## 字数控制问题

### 问题7：生成的文章字数超出范围

**症状**：
- 目标6000-8000字，实际生成了10000字
- 或者字数不足

**原因**：
- 写作过程中未实时控制字数
- 某些章节过于详细或简略

**解决方案**：

**预防措施**：

1. **在写作前规划章节字数**：

```
目标总字数：7000字
- 引言：500字
- 第一部分：1500字
- 第二部分：2000字
- 第三部分：2000字
- 第四部分：800字
- 结语：200字
```

2. **写作中实时检查**：

```bash
# 检查当前字数
python .claude/skills/article-writer/scripts/count_words.py article_output/final_article.md
```

3. **超出后调整**：
   - 删减过于详细的例子
   - 合并重复的说明
   - 精简过渡段落

---

## 依赖安装问题

### 问题8：WeasyPrint安装失败

**症状**：
- `pip install weasyprint`失败
- 提示缺少系统依赖

**原因**：
- WeasyPrint需要系统级依赖（如Cairo, Pango等）

**解决方案**：

**Ubuntu/Debian**：

```bash
# 1. 安装系统依赖
sudo apt-get update
sudo apt-get install -y \
  python3-pip \
  python3-cffi \
  python3-brotli \
  libpango-1.0-0 \
  libpangoft2-1.0-0 \
  libcairo2 \
  libgdk-pixbuf2.0-0 \
  libffi-dev \
  shared-mime-info

# 2. 安装Python包
pip install weasyprint

# 3. 验证安装
python -c "import weasyprint; print(weasyprint.__version__)"
```

**macOS**：

```bash
# 使用Homebrew安装依赖
brew install cairo pango gdk-pixbuf libffi

# 安装Python包
pip install weasyprint
```

---

## 快速诊断流程

遇到问题时，按以下顺序排查：

1. **检查系统字体**
   ```bash
   fc-list :lang=zh-cn | grep -i "noto"
   ```

2. **检查emoji字符**
   ```bash
   python .claude/skills/article-writer/scripts/remove_emoji.py article_output/final_article.md
   ```

3. **检查图片位置**
   ```bash
   grep -B 3 "!\[\]" article_output/final_article.md | grep "^##"
   ```

4. **检查PDF配置**
   ```bash
   cat .claude/skills/article-writer/scripts/generate_pdf.py | grep -A 5 "@page"
   ```

5. **重新生成PDF**
   ```bash
   python .claude/skills/article-writer/scripts/generate_pdf.py \
     article_output/final_article.md \
     article_output/final_article.pdf \
     --images-dir article_output/images/ \
     --font-family "Noto Sans CJK SC" \
     --chinese-punctuation
   ```

---

## 获取帮助

如果以上方案都无法解决问题：

1. 查看详细日志
   ```bash
   python .claude/skills/article-writer/scripts/generate_pdf.py \
     article_output/final_article.md \
     article_output/final_article.pdf 2>&1 | tee pdf_gen.log
   ```

2. 检查依赖版本
   ```bash
   pip list | grep -E "weasyprint|markdown2"
   ```

3. 提Issue到GitHub仓库（包含日志和错误信息）

---

**最后更新**：2026-01-09
**版本**：1.0
