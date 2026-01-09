#!/usr/bin/env python3
"""
Emoji移除工具
用于清除Markdown文件中的emoji字符，避免PDF生成时出现乱码

使用方法：
    python remove_emoji.py input.md [output.md]

如果不指定output.md，会直接覆盖输入文件（会先备份为.bak）
"""

import re
import sys
import shutil
from pathlib import Path


def remove_emojis(text):
    """移除所有emoji字符和特殊符号"""

    # Unicode emoji范围
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"  # dingbats
        u"\U000024C2-\U0001F251"  # enclosed characters
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess Symbols
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U00002600-\U000026FF"  # Miscellaneous Symbols
        u"\U00002700-\U000027BF"  # Dingbats
        "]+",
        flags=re.UNICODE,
    )

    # 移除emoji
    text = emoji_pattern.sub(r"", text)

    # 移除常见的unicode符号（这些在某些字体中可能显示不正确）
    problematic_chars = {
        "✅": "",  # check mark
        "☑": "",  # ballot box with check
        "✓": "",  # check mark
        "✔": "",  # heavy check mark
        "❌": "",  # cross mark
        "✗": "",  # ballot x
        "✘": "",  # heavy ballot x
        "⭐": "",  # star
        "🎯": "",  # direct hit
        "📊": "",  # bar chart
        "📈": "",  # chart increasing
        "📉": "",  # chart decreasing
        "🎨": "",  # artist palette
        "🖼": "",  # framed picture
        "💡": "",  # light bulb
        "🔍": "",  # magnifying glass
        "🔧": "",  # wrench
        "⚙": "",  # gear
        "🎭": "",  # performing arts
        "🎪": "",  # circus tent
        "💼": "",  # briefcase
        "📱": "",  # mobile phone
        "💻": "",  # laptop
        "⏰": "",  # alarm clock
        "🚀": "",  # rocket
        "🔒": "",  # locked
        "🔓": "",  # unlocked
        "📢": "",  # loudspeaker
        "📣": "",  # megaphone
        "🛒": "",  # shopping cart
        "💰": "",  # money bag
        "💵": "",  # dollar banknote
        "🎉": "",  # party popper
        "🎊": "",  # confetti ball
    }

    for char, replacement in problematic_chars.items():
        text = text.replace(char, replacement)

    return text


def count_emojis(text):
    """统计文本中的emoji数量"""
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001F900-\U0001F9FF"
        u"\U0001FA00-\U0001FA6F"
        u"\U0001FA70-\U0001FAFF"
        u"\U00002600-\U000026FF"
        u"\U00002700-\U000027BF"
        "]+",
        flags=re.UNICODE,
    )

    matches = emoji_pattern.findall(text)

    # 也计算特殊字符
    special_chars = ["✅", "☑", "✓", "✔", "❌", "✗", "✘"]
    special_count = sum(text.count(char) for char in special_chars)

    return len(matches) + special_count


def main():
    if len(sys.argv) < 2:
        print("用法：python remove_emoji.py <input.md> [output.md]")
        print()
        print("示例：")
        print("  python remove_emoji.py article.md              # 覆盖原文件（会备份）")
        print("  python remove_emoji.py article.md clean.md     # 输出到新文件")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(f"❌ 错误：找不到文件 {input_file}")
        sys.exit(1)

    # 读取文件
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 统计emoji数量
    emoji_count = count_emojis(content)

    if emoji_count == 0:
        print(f"✅ 文件中没有emoji字符，无需处理")
        return

    print(f"🔍 找到 {emoji_count} 个emoji字符")

    # 移除emoji
    cleaned = remove_emojis(content)

    # 确定输出文件
    if len(sys.argv) > 2:
        output_file = Path(sys.argv[2])
    else:
        # 备份原文件
        backup_file = input_file.with_suffix(input_file.suffix + ".bak")
        shutil.copy2(input_file, backup_file)
        print(f"📦 原文件已备份到：{backup_file}")
        output_file = input_file

    # 写入清理后的内容
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned)

    # 验证
    cleaned_count = count_emojis(cleaned)
    print(f"✅ Emoji已移除")
    print(f"📄 输出文件：{output_file}")
    print(f"📊 移除前：{emoji_count} 个emoji")
    print(f"📊 移除后：{cleaned_count} 个emoji")

    if cleaned_count > 0:
        print(f"⚠️  警告：仍有 {cleaned_count} 个emoji未能移除")


if __name__ == "__main__":
    main()
