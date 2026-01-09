# Getting Started with Claude Skills

Welcome to the Claude Skills Collection! This guide will help you get up and running with the published skills.

## 🚀 Quick Start (5 minutes)

### Option 1: Download Article Writer (Recommended)

The Article Writer skill is our most comprehensive and popular skill.

1. **Download the skill**
   ```bash
   # Create directory for Claude skills
   mkdir -p ~/.claude/skills

   # Copy the Article Writer skill
   cp -r repository/publish/claude-skills/article-writer ~/.claude/skills/
   ```

2. **Install dependencies**
   ```bash
   cd ~/.claude/skills/article-writer/scripts
   pip install -r requirements.txt
   ```

3. **Configure MCP (Required for image generation)**
   ```bash
   # Edit your MCP settings file (~/.claude/mcp_settings.json)
   # Add the nano-banana configuration:

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

4. **Restart Claude** and try the skill:
   ```
   用article-writer处理这个PDF，写一篇6000-8000字的文章
   文件：./your-document.pdf
   ```

### Option 2: Explore All Skills

```bash
# List all available skills
ls repository/publish/claude-skills/

# Get detailed information about a skill
cat repository/publish/claude-skills/[skill-name]/README.md
```

---

## 🔧 System Requirements

### Minimum Requirements

- **Claude Desktop** or **Claude Code** environment
- **Python 3.8+** (for skills with scripts)
- **4GB RAM** minimum, 8GB recommended
- **Internet connection** (for MCP server-based features)

### Recommended Setup

- **Python 3.10+** for best compatibility
- **Node.js 18+** (for MCP nano-banana)
- **PDF processing libraries** (installed automatically)
- **Chinese fonts** (for Article Writer PDF output)

### Platform Support

✅ **macOS**: Fully supported
✅ **Linux (Ubuntu/Debian)**: Fully supported
✅ **Windows**: Supported via WSL
⚠️ **Windows native**: Limited support (use WSL)

---

## 📦 Installation Guide

### Step 1: Prepare Your Environment

```bash
# Create Claude skills directory
mkdir -p ~/.claude/skills

# Ensure Python is available
python --version  # Should be 3.8+

# Optional: Create a virtual environment per skill
# python -m venv ~/.claude/skills/article-writer/venv
# source ~/.claude/skills/article-writer/venv/bin/activate
```

### Step 2: Install a Skill

```bash
# Choose a skill directory name
SKILL_NAME="article-writer"

# Copy skill to Claude directory
cp -r repository/publish/claude-skills/$SKILL_NAME ~/.claude/skills/

# Navigate to skill directory
cd ~/.claude/skills/$SKILL_NAME

# Review the skill documentation
cat README.md | head -20

# Install Python dependencies
cd scripts
pip install -r requirements.txt
```

### Step 3: Configure MCP Servers

Some skills require MCP server configurations for enhanced functionality.

#### Nano-banana (Image Generation)

```json
// File: ~/.claude/mcp_settings.json
{
  "nano-banana": {
    "command": "npx",
    "args": ["-y", "mcp-server-nano-banana"],
    "env": {
      "DUOMI_API_TOKEN": "GET_YOUR_TOKEN_FROM_DUOMI"
    },
    "disabled": false,
    "autoApprove": ["generate_image"]
  }
}
```

**Getting a DUOMI token:**
1. Visit [DUOMI Console](https://console.duomi.ai/)
2. Create account/Login
3. Generate API key
4. Replace `"GET_YOUR_TOKEN_FROM_DUOMI"` with your token

---

## 🎯 Usage Examples

### Article Writer - Complete Workflow

```
# Step 1: Ask Claude to use the skill
"用article-writer处理这个PDF，写一篇6000-8000字的科普文章
文件：./research_paper.pdf"

# Step 2: Claude will:
# - Extract PDF content
# - Generate deep analysis
# - Ask for your confirmation
# - Create New Yorker-style illustrations
# - Write the article
# - Produce final Markdown + PDF

# Result: Complete article ready for publication
```

### Article Writer - Cover Image Only

```
"帮我生成一张封面图
主题：人工智能如何改变医疗诊断
风格：科技感"
```

---

## 🛠️ Troubleshooting

### Common Issues

#### "ImportError: No module named..."
```bash
# Solution: Install dependencies
cd ~/.claude/skills/[skill-name]/scripts
pip install -r requirements.txt
```

#### "MCP server connection failed"
```bash
# Check MCP configuration
cat ~/.claude/mcp_settings.json

# Verify API token
# Test MCP server manually: npx mcp-server-nano-banana
```

#### "PDF generation failed - fonts not found"
```bash
# Install Chinese fonts
# Ubuntu/Debian:
sudo apt-get install -y fonts-noto-cjk fonts-noto-cjk-extra

# macOS:
brew install --cask font-source-han-sans
```

#### "Permission denied" or "command not found"
```bash
# Ensure correct file permissions
chmod +x ~/.claude/skills/*/scripts/*.py

# If using virtual environment, activate it first
source ~/.claude/skills/[skill-name]/venv/bin/activate
```

### Getting Help

1. **Check skill-specific troubleshooting**
   ```
   cat ~/.claude/skills/[skill-name]/TROUBLESHOOTING.md
   ```

2. **Common solutions in main repo**
   ```
   cat repository/README.md  # Has troubleshooting section
   ```

3. **Community support**
   - Create an issue in the repository
   - Check existing discussions
   - Request help from maintainers

---

## 🔧 Advanced Configuration

### Virtual Environments (Recommended)

```bash
# Create virtual environment per skill
SKILL_NAME="article-writer"
python -m venv ~/.claude/skills/$SKILL_NAME/venv

# Activate before using
source ~/.claude/skills/$SKILL_NAME/venv/bin/activate

# Install dependencies in virtual env
pip install -r requirements.txt
```

### Custom MCP Configurations

```json
{
  "nano-banana": {
    "command": "npx",
    "args": ["-y", "mcp-server-nano-banana", "--quality", "high"],
    "env": {
      "DUOMI_API_TOKEN": "your_token",
      "MAX_RETRIES": "3"
    },
    "disabled": false,
    "autoApprove": ["generate_image"],
    "timeout": 120
  }
}
```

### Environment Variables

```bash
# Export environment variables before running Claude
export DUOMI_API_TOKEN="your_token_here"
export MCP_TIMEOUT="300"
```

---

## 📊 Skill Capabilities

### Article Writer

| Feature | Status | Requirements |
|---------|--------|-------------|
| PDF Text Extraction | ✅ | Python + pdfplumber |
| Deep Content Analysis | ✅ | Claude 3.5 Sonnet |
| Illustration Generation | ✅ | MCP nano-banana + token |
| Markdown Export | ✅ | Built-in |
| PDF Generation | ✅ | WeasyPrint + fonts |
| Chinese Optimization | ✅ | Font configuration |
| Word Count Control | ✅ | Script automation |
| Error Recovery | ✅ | Comprehensive handling |

---

## 🎉 Next Steps

### Start Small
1. Install Article Writer skill
2. Process a simple PDF document
3. Experiment with different word counts
4. Try generating standalone cover images

### Explore Advanced Features
- **Multi-step workflows** for complex tasks
- **Integration with other tools** in your workflow
- **Custom skill development** based on existing patterns

### Contribute Back
- **Report bugs** and issues you encounter
- **Suggest improvements** to existing skills
- **Share your own skills** with the community

### Stay Updated
- **Watch** the repository for new skills
- **Star** skills you find useful
- **Follow** releases for updates

---

Happy skill building with Claude! 🚀✨

---

*This guide was generated for the Claude Skills Collection. Last updated: 2026-01-09*