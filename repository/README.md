# Claude Skills Collection

A curated collection of powerful Claude skills that enhance your AI-assisted development workflow. These skills are designed to help developers and content creators leverage Claude's capabilities for complex, multi-step tasks while maintaining security and best practices.

## 🔧 Skills Available

### Article Writer 📝
**Transform PDF documents into engaging Chinese popular science articles**

- **Status**: ✅ Complete and Production Ready
- **Version**: 1.0.0
- **Location**: [/publish/claude-skills/article-writer/](/publish/claude-skills/article-writer/)

#### Features
- 📄 Automated PDF content extraction and analysis
- 🎨 AI-generated illustrations (New Yorker style via MCP nano-banana)
- 📊 Word count control (4,000 - 12,000 words)
- 🀄 Chinese language optimization with proper punctuation
- 📱 Mobile-friendly PDF output
- 🖥️ Complete workflow from document to published article

#### Use Cases
- Academic paper summaries
- Technical documentation
- Scientific research popularization
- Blog content creation

---

## 🚀 Getting Started

### Prerequisites

- **Claude Desktop** or **Claude Code** environment
- **Python 3.8+** for skill scripts
- **MCP nano-banana** configuration (for image generation skills)

### Installation

1. **Clone or download** the skills you want to use
2. **Copy** the skill folder to your `.claude/skills/` directory
3. **Install dependencies** (see individual skill READMEs)
4. **Configure MCP servers** (if required)

### Quick Setup Example

```bash
# Example for Article Writer skill
cp -r article-writer ~/.claude/skills/
cd ~/.claude/skills/article-writer/scripts
pip install -r requirements.txt
```

---

## 📚 Skills Philosophy

### Design Principles

✨ **Multi-step Complexity**
- Skills handle complex workflows that require multiple sequential steps
- Each step builds on previous results with appropriate error handling

🛡️ **Security First**
- No sensitive data in example configurations
- Clear token placeholder instructions
- MCP server best practices

🎯 **User Experience Focused**
- Clear progress indicators
- Helpful error messages and troubleshooting guides
- Flexible usage patterns

📖 **Well Documented**
- Comprehensive READMEs for each skill
- Usage examples and workflows
- Troubleshooting guides included

---

## 📂 Repository Structure

```
repository/
├── README.md                    # This file
├── CONTRIBUTING.md             # Guidelines for contributors
├── LICENSE                     # MIT License
└── publish/
    └── claude-skills/
        └── [skill-name]/
            ├── SKILL.md        # Skill definition for Claude
            ├── README.md       # Detailed usage guide
            ├── scripts/        # Python utility scripts
            │   ├── requirements.txt
            │   └── [tool].py
            └── [assets]        # Skill-specific assets
```

---

## 🤝 Contributing

### Adding New Skills

1. **Fork** this repository
2. **Create** a new skill in `publish/claude-skills/[skill-name]/`
3. **Follow** the established structure and documentation standards
4. **Test** thoroughly before submitting
5. **Submit** a pull request with detailed description

### Skill Requirements

✅ **Must Have**
- Complete SKILL.md definition
- Comprehensive README.md
- All dependencies listed
- No hardcoded sensitive data
- Error handling and user-friendly messages

✅ **Should Have**
- Troubleshooting guide
- Usage examples
- Cross-platform compatibility
- Progress indicators for multi-step processes

For detailed contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 🔒 Security & Privacy

### Best Practices

- **Tokens**: Never commit real API tokens or sensitive credentials
- **Data Handling**: Skills should handle user data responsibly
- **MCP Servers**: Use established, trusted MCP server implementations
- **Review Process**: All skills undergo security review before acceptance

### MCP Server Safety

All skills using external MCP servers follow these guidelines:
- Clear documentation for required configurations
- Explicit user consent for potentially impactful operations
- Safe defaults with user override capability
- Transparent data usage disclosure

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Claude Team**: For the innovative AI assistant platform
- **MCP Community**: For the Model Context Protocol enabling these integrations
- **Contributors**: For sharing their expertise and creativity
- **DUOMI**: For the excellent nano-banana image generation service

---

## 📞 Support

- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)
- **Wiki**: [Documentation Wiki](../../wiki)

Need help with a specific skill? Check its individual README.md and TROUBLESHOOTING.md files.

---

Happy Skill Building! 🚀✨