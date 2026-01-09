#!/usr/bin/env python3
"""
中文字数统计脚本
准确统计中文文章字数（包括中英文）
"""

import sys
import argparse
import re
from pathlib import Path


def count_chinese_chars(text):
    """统计中文字符数"""
    return sum(1 for char in text if '\u4e00' <= char <= '\u9fff')


def count_english_words(text):
    """统计英文单词数"""
    # 移除中文字符
    text_without_chinese = re.sub(r'[\u4e00-\u9fff]', ' ', text)
    # 按空格和标点分割
    words = re.findall(r'\b[a-zA-Z]+\b', text_without_chinese)
    return len(words)


def count_paragraphs(text):
    """统计段落数"""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return len(paragraphs)


def count_sentences(text):
    """统计句子数"""
    # 简单统计：按中英文句号、问号、感叹号分割
    sentences = re.split(r'[。！？.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return len(sentences)


def remove_markdown_syntax(text):
    """移除Markdown语法，只保留正文"""
    # 移除代码块
    text = re.sub(r'```[\s\S]*?```', '', text)
    # 移除行内代码
    text = re.sub(r'`[^`]+`', '', text)
    # 移除图片
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', text)
    # 移除链接但保留文字
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # 移除标题标记
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    # 移除粗体、斜体标记
    text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^\*]+)\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    # 移除分隔线
    text = re.sub(r'^-{3,}$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^═{3,}$', '', text, flags=re.MULTILINE)

    return text


def analyze_text(file_path, remove_markdown=True):
    """分析文本文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    original_text = text

    if remove_markdown:
        text = remove_markdown_syntax(text)

    # 统计各项指标
    chinese_chars = count_chinese_chars(text)
    english_words = count_english_words(text)
    total_words = chinese_chars + english_words
    paragraphs = count_paragraphs(text)
    sentences = count_sentences(text)
    total_chars = len(text)
    total_chars_original = len(original_text)

    # 估算阅读时间（中文约300字/分钟）
    reading_time_min = total_words / 300
    reading_time_max = total_words / 250

    return {
        'chinese_chars': chinese_chars,
        'english_words': english_words,
        'total_words': total_words,
        'paragraphs': paragraphs,
        'sentences': sentences,
        'total_chars': total_chars,
        'total_chars_original': total_chars_original,
        'reading_time_min': reading_time_min,
        'reading_time_max': reading_time_max,
    }


def format_number(num):
    """格式化数字，添加千位分隔符"""
    return f"{num:,}"


def main():
    parser = argparse.ArgumentParser(description='统计中文文章字数')
    parser.add_argument('file_path', help='文本文件路径')
    parser.add_argument('--keep-markdown', action='store_true',
                       help='保留Markdown语法（不移除）')
    parser.add_argument('--json', action='store_true',
                       help='以JSON格式输出')

    args = parser.parse_args()

    # 检查文件
    file_path = Path(args.file_path)
    if not file_path.exists():
        print(f"❌ 错误：找不到文件：{file_path}")
        sys.exit(1)

    try:
        # 分析文本
        stats = analyze_text(file_path, remove_markdown=not args.keep_markdown)

        if args.json:
            # JSON格式输出
            import json
            print(json.dumps(stats, indent=2, ensure_ascii=False))
        else:
            # 友好格式输出
            print()
            print("=" * 60)
            print(f"  文件：{file_path.name}")
            print("=" * 60)
            print()
            print("📊 字数统计：")
            print(f"  • 中文字符：{format_number(stats['chinese_chars'])} 字")
            print(f"  • 英文单词：{format_number(stats['english_words'])} 词")
            print(f"  • 总字数：{format_number(stats['total_words'])} 字")
            print()
            print("📝 结构统计：")
            print(f"  • 段落数：{format_number(stats['paragraphs'])} 段")
            print(f"  • 句子数：{format_number(stats['sentences'])} 句")
            print(f"  • 总字符：{format_number(stats['total_chars'])} 字符")
            if not args.keep_markdown:
                print(f"  • 原始字符（含Markdown）：{format_number(stats['total_chars_original'])} 字符")
            print()
            print("⏱️  阅读时间：")
            print(f"  • 预计阅读：{stats['reading_time_min']:.1f} - {stats['reading_time_max']:.1f} 分钟")
            print(f"  • 约 {int(round(stats['reading_time_min'] + stats['reading_time_max']) / 2)} 分钟")
            print()
            print("=" * 60)

    except Exception as e:
        print(f"\n❌ 分析失败：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
