#!/usr/bin/env python3
"""
PDF文本提取脚本
从PDF文档中提取所有文本内容，保持段落结构
"""

import sys
import argparse
from pathlib import Path

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    from PyPDF2 import PdfReader
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False


def extract_with_pdfplumber(pdf_path):
    """使用pdfplumber提取文本（推荐，效果更好）"""
    text_lines = []

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"📄 PDF总页数：{total_pages}")

        for page_num, page in enumerate(pdf.pages, 1):
            print(f"⏳ 处理第 {page_num}/{total_pages} 页...", end='\r')

            # 提取文本
            page_text = page.extract_text()

            if page_text:
                # 添加页码标记
                text_lines.append(f"\n{'='*60}\n")
                text_lines.append(f"第 {page_num} 页\n")
                text_lines.append(f"{'='*60}\n\n")
                text_lines.append(page_text)
                text_lines.append("\n")

        print()  # 换行

    return ''.join(text_lines), total_pages


def extract_with_pypdf2(pdf_path):
    """使用PyPDF2提取文本（备选方案）"""
    text_lines = []

    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    print(f"📄 PDF总页数：{total_pages}")

    for page_num, page in enumerate(reader.pages, 1):
        print(f"⏳ 处理第 {page_num}/{total_pages} 页...", end='\r')

        # 提取文本
        page_text = page.extract_text()

        if page_text:
            # 添加页码标记
            text_lines.append(f"\n{'='*60}\n")
            text_lines.append(f"第 {page_num} 页\n")
            text_lines.append(f"{'='*60}\n\n")
            text_lines.append(page_text)
            text_lines.append("\n")

    print()  # 换行

    return ''.join(text_lines), total_pages


def count_chinese_chars(text):
    """统计中文字符数"""
    return sum(1 for char in text if '\u4e00' <= char <= '\u9fff')


def count_words(text):
    """统计总字数（包括中英文）"""
    # 简单统计：中文字符 + 英文单词
    chinese_chars = count_chinese_chars(text)
    # 简化处理：按空格分隔的非中文部分作为英文单词
    words = text.split()
    english_words = sum(1 for word in words if not any('\u4e00' <= char <= '\u9fff' for char in word))
    return chinese_chars + english_words


def main():
    parser = argparse.ArgumentParser(description='从PDF提取文本')
    parser.add_argument('pdf_path', help='PDF文件路径')
    parser.add_argument('output_path', help='输出文本文件路径')
    parser.add_argument('--method', choices=['pdfplumber', 'pypdf2', 'auto'],
                       default='auto', help='提取方法（默认：auto）')

    args = parser.parse_args()

    # 检查输入文件
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"❌ 错误：找不到PDF文件：{pdf_path}")
        sys.exit(1)

    # 创建输出目录
    output_path = Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"📚 开始提取PDF文本...")
    print(f"📂 输入文件：{pdf_path}")
    print(f"📝 输出文件：{output_path}")
    print()

    # 选择提取方法
    method = args.method
    if method == 'auto':
        if PDFPLUMBER_AVAILABLE:
            method = 'pdfplumber'
            print("✓ 使用pdfplumber提取（推荐）")
        elif PYPDF2_AVAILABLE:
            method = 'pypdf2'
            print("✓ 使用PyPDF2提取（备选）")
        else:
            print("❌ 错误：未安装PDF处理库")
            print("请运行：pip install pdfplumber PyPDF2")
            sys.exit(1)

    # 提取文本
    try:
        if method == 'pdfplumber':
            if not PDFPLUMBER_AVAILABLE:
                print("❌ 错误：pdfplumber未安装")
                print("请运行：pip install pdfplumber")
                sys.exit(1)
            text, total_pages = extract_with_pdfplumber(pdf_path)
        else:  # pypdf2
            if not PYPDF2_AVAILABLE:
                print("❌ 错误：PyPDF2未安装")
                print("请运行：pip install PyPDF2")
                sys.exit(1)
            text, total_pages = extract_with_pypdf2(pdf_path)

        # 保存文本
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)

        # 统计信息
        total_chars = len(text)
        chinese_chars = count_chinese_chars(text)
        total_words = count_words(text)
        paragraphs = len([p for p in text.split('\n\n') if p.strip()])

        print()
        print("✅ 提取完成！")
        print()
        print("📊 统计信息：")
        print(f"  • 总页数：{total_pages}")
        print(f"  • 总字符：{total_chars:,}")
        print(f"  • 中文字符：{chinese_chars:,}")
        print(f"  • 总字数（估算）：{total_words:,}")
        print(f"  • 段落数：{paragraphs}")
        print()
        print(f"  输出文件：{output_path}")

        # 预览前200字
        preview = text.strip()[:200].replace('\n', ' ')
        print()
        print("📖 前200字预览：")
        print("─" * 60)
        print(preview + "...")
        print("─" * 60)

    except Exception as e:
        print(f"\n❌ 提取失败：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
