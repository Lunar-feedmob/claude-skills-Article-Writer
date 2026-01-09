---
name: article-writer
description: Transform PDF documents into engaging Chinese popular science articles. Extracts content, analyzes deeply, writes in conversational style with analogies, generates New Yorker-style illustrations via MCP nano-banana, outputs PDF and Markdown. Features customizable word count, standalone cover generation, natural flow with Chinese punctuation.
allowed-tools: Read, Write, Bash(python:*), mcp__nano-banana__generate_image
model: claude-sonnet-4-5-20250929
---

# Article Writer - 深度科普文章创作助手

将PDF文档转化为引人入胜的中文科普深度解读，采用口语化写作风格，配以类比和清晰解释，生成纽约客风格插图，输出PDF和Markdown格式。

## 核心特性

✨ **可定制字数**：支持6000-8000字或自定义字数
🎨 **独立封面生成**：可单独生成文章封面图
🇨🇳 **中文优先**：使用中文和中文标点符号
💬 **口语化表达**：自然流畅，易于理解的科普风格
📚 **教学式讲解**：用类比让复杂概念变简单
🖼️ **纽约客插图**：简洁线条艺术风格（MCP nano-banana生成）

## 写作风格要求（核心原则）

### 语言风格

**✅ 使用**：
- 中文表达和中文标点符号（，。！？：；""''）
- 口语化用词，像和朋友聊天一样自然
- 短句为主，避免冗长复杂的句子
- 多用"你可以这样理解""打个比方""简单来说"等过渡
- 用"我们""咱们"拉近与读者距离

**❌ 避免**：
- 生硬的学术腔调
- 过长的从句套从句
- 罕见的书面语词汇
- 英文标点符号（除非在英文术语中）

### 类比和解释

每个复杂概念必须：
1. 先给一句话定义
2. 再用日常生活类比
3. 展开类比，建立直觉理解
4. 最后回到科学准确性

示例：
```
什么是轨道共振？

简单来说，就是两个天体在运行时，周期之间有个整数比关系。

打个比方，这就像两个朋友一起散步。一个人走得快，一个人走得慢，
但神奇的是，快的人每走3圈，慢的人正好走2圈。这样每隔一段时间，
他们就会在同一个地方相遇。

天体的轨道共振也是这样...
```

## 完整工作流程（8步）

### Step 0: Intelligent PDF Management

**智能PDF管理与准备**

1. **接收PDF文件**

   询问用户：
   ```
   📄 请提供要解读的PDF文档：

   方式1：文件路径（例如：./research_paper.pdf）
   方式2：文件名（我会在当前目录搜索）

   请提供PDF路径或文件名：
   ```

2. **询问文章字数偏好**

   ```
   📏 请选择文章字数范围：

   1. 标准版（6000-8000字）- 深度解读，适合15-20分钟阅读
   2. 精华版（4000-6000字）- 核心要点，适合10-15分钟阅读
   3. 深度版（8000-12000字）- 全面剖析，适合25-30分钟阅读
   4. 自定义（请告诉我目标字数）

   请选择 1、2、3 或告诉我具体字数：
   ```

   记录用户选择的字数范围。

3. **验证文件并创建工作空间**

   ```bash
   # 检查文件
   ls -lh "$PDF_PATH"

   # 创建输出目录结构
   mkdir -p article_output/{images,charts,text,analysis}
   ```

4. **文件信息报告**

   ```
   ✅ PDF已就绪

   📄 文件信息：
   - 文件名：[name]
   - 大小：[size] MB
   - 目标字数：[word_count_range]

   开始7步创作流程...
   ```

---

### Step 1: Extract PDF Text

**提取PDF完整文本**

执行文本提取：

```bash
python .claude/skills/article-writer/scripts/extract_text.py \
  "$PDF_PATH" \
  article_output/text/extracted_text.txt
```

脚本功能：
- 提取所有文本内容
- 保持段落结构和层次
- 识别标题和章节
- 处理多栏排版

提取完成后报告：

```
✅ Step 1 完成：文本提取

📝 提取统计：
- 总页数：[pages]
- 总字数：[words]
- 段落数：[paragraphs]
- 输出：article_output/text/extracted_text.txt
```

---

### Step 5: Extract Charts in Advance

**提前提取图表和图片**

注意：跳到Step 5，先提取视觉元素以辅助后续理解。

```bash
python .claude/skills/article-writer/scripts/extract_charts.py \
  "$PDF_PATH" \
  article_output/charts/
```

脚本功能：
- 提取所有图片、图表、示意图
- 按页码自动命名
- 识别图表类型
- 生成图表清单JSON

完成后报告：

```
✅ Step 5 完成：图表提取

📊 提取结果：
- 图表数量：[count]
- 保存位置：article_output/charts/

图表清单：
[page_1] Figure 1: [description]
[page_3] Figure 2: [description]
...
```

---

### Step 2: Generate Complete Interpretation

**生成完整的深度解读分析**

现在回到Step 2，结合文本和图表进行全面分析，生成分析文档。

详细流程包括：
- 核心问题识别
- 内容结构解析
- 关键概念提取（准备类比）
- 论点论证链条分析
- 数据图表深度解读
- 创新点识别

生成：`article_output/analysis/deep_analysis.md`

然后与用户确认创作方向：

```
✅ Step 2 完成：深度解读分析

📖 已生成完整分析文档

💡 建议的文章方向：

**标题**：[吸引人的中文标题]

**定位**：[读者群体]

**字数**：[根据用户选择的范围]

**结构**：[X]个部分

**风格**：口语化科普，丰富类比，自然流畅

请问您希望：
1. ✅ 按照建议方向开始创作
2. 🔧 调整创作方向
3. 📄 先查看完整分析文档

请回复 1、2 或 3
```

等待用户确认。

---

### Step 5.5: Generate "The New Yorker" Illustrations

**使用MCP nano-banana生成纽约客风格插图**

确认后，开始生成文章配图。

#### 插图生成方案

根据文章字数，规划插图数量：
- 4000-6000字：4-5张插图（封面+3-4张段落图）
- 6000-8000字：5-6张插图（封面+4-5张段落图）
- 8000-12000字：6-8张插图（封面+5-7张段落图）

#### 纽约客风格特征

所有插图统一风格：
- ✏️ 简洁的线条艺术
- 🎨 有限色彩（通常2-3种颜色）
- 💡 聪明的视觉隐喻
- 😊 略带幽默或思考性
- 📐 干净的构图

#### 插图类型

1. **封面图** (Cover Illustration)
   - 尺寸：16:9（适合公众号首图）
   - 用途：代表文章核心主题
   - 特点：最吸引眼球，视觉冲击力强

2. **段落配图** (Section Illustrations)
   - 尺寸：1:1 或 4:3
   - 用途：辅助理解各部分内容
   - 特点：简洁明了，呼应文字

3. **数据可视化插图** (Data Visualization)
   - 尺寸：16:9
   - 用途：艺术化呈现数据图表
   - 特点：保留数据信息，提升美感

#### 生成流程

向用户展示计划：

```
🎨 插图生成计划

计划生成 [count] 张插图：

📸 1. 封面图
   主题：[核心主题的视觉呈现]
   隐喻：[视觉元素]
   尺寸：16:9

📸 2-N. 段落配图
   [列出每张图的主题和隐喻]

风格：纽约客杂志风格
- 简洁线条
- 2-3种颜色
- 聪明隐喻

使用：MCP nano-banana生成

是否开始生成？
```

#### 使用MCP nano-banana生成图片

用户确认后，逐张生成。对于每张图：

**1. 准备详细的英文prompt**

```
封面图prompt示例：

"A minimalist New Yorker magazine style illustration depicting [主题].
Clean line art with simple geometric shapes, limited color palette of
black, white, and one accent color (deep blue or warm orange).
The composition shows [场景描述], creating a clever visual metaphor
for [概念]. Sophisticated yet accessible, with a touch of wit and humor.
Professional editorial illustration style for Chinese science article cover.
Aspect ratio 16:9, high resolution."
```

**2. 调用MCP nano-banana生成图片**

使用MCP tool：`mcp__nano-banana__generate_image`

参数：
- `prompt`：详细的英文prompt
- `aspect_ratio`："16:9" 或 "1:1"
- `resolution`："high" 或 "1080p"

示例：

```
调用：mcp__nano-banana__generate_image

参数：
{
  "prompt": "A minimalist New Yorker style illustration showing orbital resonance...",
  "aspect_ratio": "16:9",
  "resolution": "1080p"
}
```

**3. 保存生成的图片**

MCP会返回生成的图片，保存到输出目录：

```bash
# MCP返回的图片保存为
mv [mcp_generated_image_path] article_output/images/01_cover_illustration.png
```

**4. 生成下一张图片**

重复步骤1-3，生成所有规划的插图：

```
🎨 插图生成进度：

✅ 1/6 封面图 - 已完成
   → 01_cover_illustration.png

✅ 2/6 第一部分 - 已完成
   → 02_section1_illustration.png

⏳ 3/6 第二部分 - 生成中...

⬜ 4/6 第三部分 - 等待中
⬜ 5/6 数据可视化 - 等待中
⬜ 6/6 总结图 - 等待中
```

#### 完成报告

```
✅ Step 5.5 完成：纽约客风格插图生成

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎨 已生成 [6] 张插图：

1. ✓ 01_cover_illustration.png
   封面图 - [主题描述]

2. ✓ 02_section1_illustration.png
   第一部分 - [主题描述]

3. ✓ 03_section2_illustration.png
   第二部分 - [主题描述]

4. ✓ 04_section3_illustration.png
   第三部分 - [主题描述]

5. ✓ 05_datavis_illustration.png
   数据可视化 - [主题描述]

6. ✓ 06_summary_illustration.png
   总结图 - [主题描述]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

生成方式：MCP nano-banana
保存位置：article_output/images/
风格：纽约客杂志插图风格
尺寸：优化为公众号推荐尺寸

准备进入Step 6：撰写文章并整合插图
```

---

### Step 5.5 附加功能：单独生成封面图

**独立封面图生成模式**

如果用户只想生成封面图（不生成完整文章），可以单独执行：

```
🎨 独立封面图生成模式

我将使用MCP nano-banana为您的文章生成封面图。

请告诉我：
1. 文章的核心主题或标题
2. 希望传达的感觉（科技感/温馨/严肃/幽默等）
3. 偏好的颜色（如果有）

或者，如果您已经有完整的构思，直接告诉我您的想法。
```

收集信息后：

1. **设计封面方案**

   ```
   📸 封面图设计方案

   主题：[用户提供的主题]
   视觉隐喻：[设计的隐喻方案]
   色彩方案：[建议的配色]
   构图：[构图描述]

   风格：纽约客杂志插图
   - 简洁线条艺术
   - [2-3]种颜色
   - 聪明的视觉表达

   是否满意这个方案？
   ```

2. **使用MCP生成封面图**

   ```
   调用：mcp__nano-banana__generate_image

   prompt: "A minimalist New Yorker magazine style cover illustration
   depicting [主题描述]. Clean line art with simple geometric shapes,
   limited color palette of [colors]. The composition shows [场景描述],
   creating a clever visual metaphor for [概念]. Sophisticated yet
   accessible, with a touch of wit. Aspect ratio 16:9, high resolution,
   professional editorial illustration style for Chinese WeChat article cover."

   aspect_ratio: "16:9"
   resolution: "1080p"
   ```

3. **保存和预览**

   ```bash
   mv [mcp_generated] article_output/images/standalone_cover.png
   ```

   ```
   ✅ 封面图已生成！

   📁 文件位置：article_output/images/standalone_cover.png
   📐 尺寸：16:9（适合公众号）
   🎨 风格：纽约客插图风格
   🔧 生成方式：MCP nano-banana

   您可以：
   - 查看图片
   - 调整设计方案重新生成
   - 生成多个版本供选择
   ```

4. **可选：生成多个版本**

   如果用户想要多个选项：

   ```
   要不要我生成几个不同版本的封面图，让您选择？

   可以生成：
   1. 不同视觉隐喻的版本
   2. 不同配色方案的版本
   3. 不同构图的版本

   请告诉我您的偏好。
   ```

   然后生成2-3个版本：

   ```
   ✅ 已生成3个封面图版本：

   1. standalone_cover_v1.png - [方案A描述]
   2. standalone_cover_v2.png - [方案B描述]
   3. standalone_cover_v3.png - [方案C描述]

   请告诉我您喜欢哪一个，或需要进一步调整。
   ```

---

### Step 6: Save Final File

**撰写最终文章并保存为Markdown和PDF**

#### 6.1 撰写文章

基于Step 2的分析和Step 5.5的插图，撰写完整文章。

**核心写作原则**：

1. **严格控制字数**
   - 根据用户选择的字数范围写作
   - 6000-8000字：深度解读，15-20分钟阅读
   - 实时检查字数，确保在范围内

2. **中文和中文标点**
   - 全文使用中文
   - 使用中文标点：，。！？：；""''
   - 英文术语用斜体或括号标注

3. **口语化科普风格**
   - 像和朋友聊天一样自然
   - 多用"你可以这样想""咱们来看看""简单来说"
   - 短句为主，避免复杂从句
   - 用"我们""咱们"拉近距离

4. **丰富的类比**
   - 每个复杂概念都有日常类比
   - 类比要贴切、生动、易懂
   - 先类比建立直觉，再深入科学细节

5. **清晰的结构**
   - 明确的章节划分
   - 过渡段落自然流畅
   - 用小标题引导阅读

**文章结构模板**：

```markdown
# [吸引人的中文标题]

![封面图](images/01_cover_illustration.png)

> **导语**：[用150-200字吸引读者，可以是故事、问题或有趣的现象]
>
> *阅读时长：约[X]分钟 | 文章字数：[XXXX]字*

---

## 引言：为什么要关注这个问题？

[用口语化的方式引入主题，可以从一个故事或现象开始]

咱们先来看一个有趣的现象...

[说明问题的重要性，为什么值得花时间了解]

你可能会好奇，这和我有什么关系？其实...

---

## 第一部分：理解背景

### 从一个例子说起

[用具体例子或类比开始]

打个比方，这就像...

### 几个关键概念

在往下聊之前，咱们得先理解几个概念：

#### **概念A**

**简单来说**：[一句话定义]

**打个比方**：[日常生活类比]

比如说，[展开类比，让读者建立直觉理解]

从科学角度看，[回归科学准确性]

#### **概念B**

[同上，用口语化方式解释]

### 问题的由来

[介绍背景，用讲故事的方式]

![第一部分插图](images/02_section1_illustration.png)
*插图：[简短说明]*

---

## 第二部分：问题的本质

### 看起来简单，其实...

[深入剖析问题，但保持口语化]

你可能觉得这很简单，不就是...吗？其实没那么容易。

为什么呢？主要有这么几个原因：

**第一个难题**：[用通俗语言描述]

这就好比...（类比）

**第二个难题**：[描述]

咱们可以这样理解...（解释）

**第三个难题**：[描述]

简单来说就是...（总结）

### 前人的尝试

[介绍现有研究，但避免学术腔]

科学家们早就在琢磨这个问题了...

![第二部分插图](images/03_section2_illustration.png)
*插图：[简短说明]*

---

## 第三部分：新的思路

### 换个角度想

[引入新方法，用讲故事的方式]

那有没有其他办法呢？咱们换个角度来看看。

[用类比解释核心思想]

你可以把它想象成...

### 这是怎么运作的？

[分步骤解释机制，保持口语化]

这个过程大概是这样的：

**第一步**：[发生了什么]

打个比方，[类比解释]

**第二步**：[接下来怎样]

简单来说，[通俗解释]

**第三步**：[最后结果]

所以呢，[总结]

### 几个关键因素

[解释重要参数，避免专业术语堆砌]

这里面有几个关键的东西：

**因素X**：[作用]
你可以理解为，[类比或通俗解释]

**因素Y**：[作用]
这就像...[类比]

![第三部分插图](images/04_section3_illustration.png)
*插图：[简短说明]*

---

## 第四部分：证据在哪里？

### 数据告诉我们什么

[介绍数据和图表，用讲故事的方式]

说了这么多，有没有证据呢？咱们来看看实际的数据。

#### 一个关键的发现

![数据插图](images/05_datavis_illustration.png)
*插图：[图表说明]*

**怎么看这张图？**

让我来带你看看这张图：

- 横轴是...[通俗解释]
- 纵轴是...[通俗解释]
- 这条线/这些点...[指出关键趋势]

**这说明了什么？**

简单来说，[通俗解释结论]

就好比...[类比帮助理解]

### 不是万能的

[讨论局限性，保持诚实和口语化]

当然啦，这个方法也不是万能的。

它有几个局限：

- [局限A]，也就是说...[解释]
- [局限B]，换句话说...[解释]

---

## 第五部分：更广阔的视野

### 这不只是一个孤立的问题

[连接到更大的图景]

你可能会想，了解这个有什么用呢？

其实意义可大了：

**对[领域A]的启发**

[展开，用通俗语言]

**对[领域B]的影响**

[展开]

**实际应用**

[举例说明实际价值]

比如说，未来可能...[具体应用场景]

![总结插图](images/06_summary_illustration.png)
*插图：[整体框架]*

### 还有哪些未解之谜

[介绍未来方向，保持好奇和开放]

科学研究就是这样，解决一个问题，又会冒出新的问题：

- [问题A]
- [问题B]
- [问题C]

这些都等着科学家们去探索。

---

## 结语

[总结全文，用简洁有力的语言]

说了这么多，咱们回到最开始的问题...

[回应开头，形成呼应]

[留下思考或展望]

下次当你...的时候，也许会想起今天聊的这些。

---

## 小贴士：你可能想问

**Q：[读者可能的疑问]**
A：[用口语化方式回答]

**Q：[疑问]**
A：[回答]

**Q：[疑问]**
A：[回答]

---

## 术语小词典

**[术语A]**：[通俗定义]

**[术语B]**：[通俗定义]

[列出关键术语]

---

## 延伸阅读

如果你对这个话题感兴趣，可以看看：

- [资源1]
- [资源2]

---

## 参考资料

本文基于：[原始PDF文档]

---

*📅 发布：[date]*
*✍️ 基于：[PDF名称]*
*🎨 配图：[count]张纽约客风格原创插图（MCP nano-banana生成）*
*📊 字数：[XXXX]字*
*⏱️ 阅读：约[X]分钟*

---

**喜欢这篇文章吗？** [分享给朋友，一起涨知识！]
```

#### 写作中的字数控制

在写作过程中，实时估算字数：

```
当前字数：[current_word_count] / 目标：[target_word_count_range]

进度：[progress_bar]
```

如果超出或不足，及时调整各部分内容的详略。

#### 6.2 保存Markdown文件

```bash
# 保存文章
cat > article_output/final_article.md << 'EOF'
[文章内容]
EOF

# 统计实际字数
python .claude/skills/article-writer/scripts/count_words.py article_output/final_article.md
```

报告：

```
✅ 文章已保存为Markdown

📝 文章统计：
- 文件：final_article.md
- 字数：[XXXX]字（目标：[range]字）✓
- 段落：[count]段
- 章节：[count]个
- 配图：[count]张
```

#### 6.3 生成PDF

```bash
python .claude/skills/article-writer/scripts/generate_pdf.py \
  article_output/final_article.md \
  article_output/final_article.pdf \
  --images-dir article_output/images/ \
  --font "Source Han Sans SC" \
  --font "Noto Serif SC" \
  --page-size A4 \
  --add-toc \
  --chinese-punctuation
```

参数说明：
- `--font`：中文字体（思源黑体、思源宋体等）
- `--chinese-punctuation`：确保中文标点正确渲染
- `--add-toc`：生成目录

PDF特性：
- ✅ 完美中文支持
- ✅ 中文标点正确显示
- ✅ 图片自动嵌入
- ✅ 美化排版
- ✅ 可点击目录

报告：

```
✅ Step 6 完成：文章撰写与保存

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 已生成文件：

1. 📝 final_article.md（Markdown）
   - 字数：[XXXX]字 ✓
   - 段落：[count]段
   - 配图：[count]张

2. 📄 final_article.pdf（PDF）
   - 大小：[size] MB
   - 页数：[pages]页
   - 中文字体：思源黑体
```

---

### Step 6.5: Layout Optimization (排版优化)

**对Markdown文件进行排版优化，确保PDF生成质量**

这是一个新增的关键步骤，用于解决实际遇到的PDF排版问题。

#### 6.5.1 检查和移除Emoji字符

**问题**：Emoji字符（如 ✅ ☑ ✓ 等）在PDF中会显示为乱码或方块

**解决方案**：扫描并移除所有emoji

```bash
# 使用grep检查是否有emoji字符
grep -P "[\x{1F300}-\x{1F9FF}\x{2600}-\x{26FF}\x{2700}-\x{27BF}]|[✅☑✓✔]" article_output/final_article.md
```

如果发现emoji，逐一替换：

```python
# 示例：移除bullet point中的emoji
旧：✅ **不可变日志**：所有交易决策...
新：**不可变日志**：所有交易决策...

旧：- ✓ 中文表达
新：- 中文表达
```

**常见emoji列表**：
- ✅ ☑ ✓ ✔ （勾选符号）
- ❌ ✗ （叉号）
- 📊 📈 📉 （图表）
- 🎨 🖼️ （艺术/图片）
- 💡 🔍 🔧 （工具/想法）
- 🎯 🎭 🎪 （目标/娱乐）

**自动化脚本建议**：

创建 `remove_emoji.py`：

```python
#!/usr/bin/env python3
import re
import sys

def remove_emojis(text):
    """移除所有emoji字符"""
    # Emoji pattern
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols
        "]+", flags=re.UNICODE)

    # 也移除常见的unicode符号
    text = text.replace('✅', '')
    text = text.replace('☑', '')
    text = text.replace('✓', '')
    text = text.replace('✔', '')
    text = text.replace('❌', '')
    text = text.replace('✗', '')

    return emoji_pattern.sub(r'', text)

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    cleaned = remove_emojis(content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned)

    print(f"✅ Emoji已移除，保存到：{output_file}")
```

#### 6.5.2 优化图片位置

**问题**：图片放置在章节开头会导致PDF出现大片留白

**最佳实践**：

1. **图片应放在段落之后**，而不是章节/小节开头
   ```markdown
   # 错误示例 ❌
   ## 第一部分：问题背景

   ![](images/01_problem.png)

   这是问题的详细描述...

   # 正确示例 ✅
   ## 第一部分：问题背景

   这是问题的详细描述，经过几段文字的铺垫后...

   [更多文字内容]

   ![](images/01_problem.png)
   <p align="center"><i>图1：问题示意图</i></p>
   ```

2. **图片前应有充实内容**（至少2-3段文字）

3. **图片说明要简洁**
   ```markdown
   ![](images/diagram.png)
   <p align="center"><i>简短说明（10字以内）</i></p>
   ```

4. **避免连续放置多张图片**，中间应穿插文字说明

**优化检查清单**：

```bash
# 检查图片位置
grep -B 3 "!\[\]" article_output/final_article.md | grep "^##"
```

如果发现图片紧跟在标题后面，需要调整位置。

#### 6.5.3 CSS和PDF生成配置优化

**关键CSS配置**（已在generate_pdf.py中实现）：

```css
/* 图片尺寸优化 */
img {
    max-width: 85%;        /* 不要100%，留出边距 */
    max-height: 400pt;     /* 限制高度避免过大 */
    margin: 12pt auto;     /* 适度边距 */
    page-break-before: avoid;  /* 避免图片前分页 */
    page-break-after: auto;    /* 允许图片后自然分页 */
}

/* 移除页码（如果不需要） */
@page {
    size: A4;
    margin: 2cm 1.5cm;
    /* 不设置 @bottom-center 就没有页码 */
}

/* 字体配置 */
body {
    font-family: "Noto Sans CJK SC", "Noto Serif CJK SC",
                 "WenQuanYi Micro Hei", "SimSun", sans-serif;
}
```

#### 6.5.4 生成PDF前的最终检查

```bash
# 1. 检查中文字体是否安装
fc-list :lang=zh-cn | grep -i "noto"

# 如果没有，安装字体
sudo apt-get install -y fonts-noto-cjk fonts-noto-cjk-extra

# 2. 生成PDF（使用优化后的配置）
python .claude/skills/article-writer/scripts/generate_pdf.py \
  article_output/final_article.md \
  article_output/final_article.pdf \
  --images-dir article_output/images/ \
  --font-family "Noto Sans CJK SC" \
  --chinese-punctuation

# 3. 检查PDF文件大小和基本信息
ls -lh article_output/final_article.pdf
file article_output/final_article.pdf
```

#### 6.5.5 排版问题诊断

如果PDF仍有问题，使用以下诊断流程：

**问题1：中文显示为方块（豆腐块）**
```bash
# 诊断
fc-list :lang=zh-cn

# 解决
sudo apt-get install -y fonts-noto-cjk fonts-wqy-microhei fonts-wqy-zenhei
fc-cache -fv
```

**问题2：图片周围有大片留白**
- 检查图片是否在章节开头
- 移动图片到段落之后
- 减小图片尺寸（CSS中max-width: 85%）

**问题3：Emoji显示为奇怪符号**
- 运行emoji检测脚本
- 手动或自动移除所有emoji字符

**问题4：页码显示**
- 检查generate_pdf.py中的@page配置
- 确保没有@bottom-center规则

#### 6.5.6 完成报告

```
✅ Step 6.5 完成：排版优化

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 检查项目：

✓ Emoji字符已移除
✓ 图片位置已优化（[X]处调整）
✓ PDF布局检查通过
✓ 中文字体配置正确
✓ 页码设置符合要求

📄 优化后的文件：
- article_output/final_article.md （已优化）
- article_output/final_article.pdf （[size] MB）

准备进入Step 7：完整交付报告
```

---

### Step 7: Final Output (最终输出)

**生成最终的Markdown和PDF文件**

如果在Step 6.5中进行了修改，需要重新生成PDF：

```bash
python .claude/skills/article-writer/scripts/generate_pdf.py \
  article_output/final_article.md \
  article_output/final_article.pdf \
  --images-dir article_output/images/ \
  --font-family "Noto Sans CJK SC" \
  --chinese-punctuation
```

```
✅ Step 7 完成：最终输出

📄 最终文件：
- article_output/final_article.md （已优化排版）
- article_output/final_article.pdf （[size] MB，无乱码，布局优化）
```

---

### Step 8: Complete Report (完成报告)

**生成完整交付报告**

```
╔══════════════════════════════════════════════════╗
║                                                  ║
║          ✅  文章创作完成！                      ║
║                                                  ║
╚══════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋  流程回顾

✅ Step 0：PDF管理 - 文件准备，字数确认
✅ Step 1：文本提取 - [pages]页，[words]字
✅ Step 5：图表提取 - [count]个图表
✅ Step 2：深度分析 - 完整解读报告
✅ Step 5.5：插图生成 - [count]张（MCP nano-banana）
✅ Step 6：文章撰写 - 初稿生成
✅ Step 6.5：排版优化 - Emoji移除、图片位置优化
✅ Step 7：最终输出 - MD + PDF
✅ Step 8：完成报告 - 当前

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦  交付文件

article_output/
├── 📝 final_article.md      ← ⭐ Markdown文章
├── 📄 final_article.pdf      ← ⭐ PDF文章
├── 📖 analysis/deep_analysis.md
├── 🎨 images/               ← [count]张插图
│   ├── 01_cover_illustration.png
│   ├── 02_section1_illustration.png
│   └── ...
├── 📊 charts/               ← 原始图表
└── 📃 text/extracted_text.txt

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊  内容统计

文章：
  • 标题：[title]
  • 字数：[XXXX]字（目标：[range]字）✓
  • 阅读时长：约[X]分钟
  • 段落数：[count]
  • 章节数：[count]

配图：
  • 插图：[count]张
  • 生成方式：MCP nano-banana
  • 风格：纽约客杂志风格
  • 尺寸：优化为公众号规格

语言：
  • ✓ 中文表达
  • ✓ 中文标点
  • ✓ 口语化科普风格
  • ✓ 丰富类比

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡  文章特色

✓ 口语化表达 - 像聊天一样自然流畅
✓ 丰富类比 - 每个复杂概念都有日常例子
✓ 短句清晰 - 避免冗长复杂句式
✓ 读者视角 - 用"我们""咱们"拉近距离
✓ 渐进讲解 - 从简单到深入层层递进
✓ 纽约客插图 - 简洁线条，聪明隐喻（MCP生成）
✓ 中文标点 - 严格使用中文标点符号

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱  公众号发布指南

1. 📄 打开 final_article.md
2. 📋 复制内容到公众号编辑器
3. 🖼️ 图片会自动上传（或手动上传images/目录）
4. 🎨 封面：使用 01_cover_illustration.png
5. 📝 摘要：可使用导语部分
6. ⏰ 建议发布时间：工作日晚8点或周末上午

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯  后续操作

您可以：
□ 预览文章
□ 微调内容
□ 重新生成某张插图
□ 调整字数
□ 单独生成新封面图

需要调整吗？随时告诉我！

╔══════════════════════════════════════════════════╗
║          创作完成，祝发布顺利！🎉              ║
╚══════════════════════════════════════════════════╝
```

---

## 独立功能：封面图生成器

除了完整的7步流程，还支持单独生成封面图。

### 使用场景

- 已有文章，只需要配封面图
- 想要多个封面方案供选择
- 更换现有文章的封面

### 使用方法

对Claude说：

```
请帮我生成一张文章封面图
主题是：[你的文章主题]
```

或者：

```
我有一篇关于[主题]的文章，想要一张纽约客风格的封面图
```

### 生成流程

1. **收集信息**
   - 文章主题或标题
   - 希望传达的感觉
   - 颜色偏好（可选）

2. **设计方案**
   - 提供视觉隐喻方案
   - 色彩搭配建议
   - 构图描述

3. **使用MCP生成图片**
   - 调用 mcp__nano-banana__generate_image
   - 保存为高分辨率16:9图片

4. **可选：多版本**
   - 生成2-3个不同方案
   - 用户选择最满意的

---

## MCP nano-banana配置

本Skills使用MCP nano-banana进行图片生成。

### 配置要求

确保MCP配置文件中包含：

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

### API Token

需要有效的DUOMI_API_TOKEN才能使用图片生成功能。

### 自动批准

`autoApprove: ["generate_image"]`确保图片生成自动执行，无需每次确认。

---

## 技术实现

### 依赖安装

```txt
# PDF处理
pdfplumber>=0.10.0
PyPDF2>=3.0.0

# 图片处理
Pillow>=10.0.0
pdf2image>=1.16.0

# PDF生成（支持中文）
markdown2>=2.4.10
weasyprint>=60.0
reportlab>=4.0.0

# Markdown处理
python-markdown>=3.5.0
pymdown-extensions>=10.0

# 中文支持
python-bidi>=0.4.2
arabic-reshaper>=3.0.0
```

安装：

```bash
pip install -r .claude/skills/article-writer/scripts/requirements.txt
```

### Python脚本

1. **extract_text.py** - PDF文本提取
2. **extract_charts.py** - 图表提取
3. **generate_pdf.py** - PDF生成（中文支持）
4. **count_words.py** - 中文字数统计
5. **utils.py** - 工具函数

---

## 使用示例

### 完整流程

```
用户：帮我处理这个PDF，写一篇6000-8000字的科普文章
      文件：./quantum_paper.pdf

助手：[执行Step 0-7]

      ✅ 文章创作完成！

      生成了一篇7200字的深度科普文章
      配有6张纽约客风格插图（MCP nano-banana生成）
      Markdown和PDF双格式

      [显示完整报告]
```

### 单独生成封面图

```
用户：帮我生成一张封面图
      主题：人工智能如何改变医疗诊断

助手：好的！让我为您设计封面图方案。

      [设计方案]
      主题：AI医疗诊断
      视觉隐喻：机器人医生用听诊器检查人体
      色彩：科技蓝 + 温暖橙
      风格：纽约客插图

      [使用MCP nano-banana生成]

      ✅ 封面图已生成！
      文件：standalone_cover.png

      需要生成其他版本吗？
```

---

## 注意事项

1. **MCP配置**：确保nano-banana MCP已正确配置
2. **API Token**：需要有效的DUOMI_API_TOKEN
3. **字数控制**：严格按用户选择的字数范围写作
4. **中文标点**：全文使用中文标点符号（，。！？：；""''）
5. **口语化**：保持自然流畅，像聊天一样
6. **类比丰富**：每个复杂概念都有通俗类比
7. **插图风格**：所有插图保持纽约客风格统一
8. **PDF字体**：确保中文字体正确安装

---

## 相关文档

- [实现细节](IMPLEMENTATION.md) - 技术文档
- [脚本说明](SCRIPTS.md) - Python脚本
- [写作指南](WRITING_GUIDE.md) - 口语化写作技巧
- [MCP配置](MCP_CONFIG.md) - nano-banana配置指南
- [FAQ](FAQ.md) - 常见问题

---

## 快速调用

对Claude说：

```
用article-writer处理这个PDF，写一篇[字数]字的文章
```

或：

```
用article-writer生成一张封面图
```

开始创作吧！📝✨
