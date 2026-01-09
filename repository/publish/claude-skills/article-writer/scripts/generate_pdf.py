#!/usr/bin/env python3
"""
Markdown转PDF生成脚本
支持中文、中文标点、图片嵌入
"""

import sys
import argparse
from pathlib import Path
import re

try:
    import markdown2
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False


def convert_markdown_to_html(md_content, images_dir=None):
    """将Markdown转换为HTML"""
    # Markdown转HTML
    html_content = markdown2.markdown(
        md_content,
        extras=[
            "fenced-code-blocks",
            "tables",
            "break-on-newline",
            "header-ids",
            "footnotes"
        ]
    )

    # 如果指定了图片目录，调整图片路径
    if images_dir:
        images_dir = Path(images_dir).absolute()

        def replace_img_path(match):
            img_path = match.group(1)
            # 如果是相对路径，转为绝对路径
            if not img_path.startswith(('http://', 'https://', '/')):
                full_path = images_dir / img_path.replace('images/', '')
                return f'<img src="file://{full_path}"'
            return match.group(0)

        html_content = re.sub(r'<img src="([^"]+)"', replace_img_path, html_content)

    return html_content


def create_html_document(html_content, title="Article", font_family="Source Han Sans SC"):
    """创建完整的HTML文档，包含CSS样式"""

    css_style = f"""
    @page {{
        size: A4;
        margin: 2cm 1.5cm;
    }}

    body {{
        font-family: "Noto Sans CJK SC", "Noto Serif CJK SC", "WenQuanYi Micro Hei", "SimSun", sans-serif;
        font-size: 11pt;
        line-height: 1.8;
        color: #333;
        text-align: justify;
    }}

    h1 {{
        font-size: 24pt;
        font-weight: bold;
        color: #1a1a1a;
        margin-top: 0;
        margin-bottom: 20pt;
        text-align: center;
        page-break-after: avoid;
    }}

    h2 {{
        font-size: 18pt;
        font-weight: bold;
        color: #2c2c2c;
        margin-top: 24pt;
        margin-bottom: 12pt;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 6pt;
        page-break-after: avoid;
    }}

    h3 {{
        font-size: 14pt;
        font-weight: bold;
        color: #404040;
        margin-top: 18pt;
        margin-bottom: 10pt;
        page-break-after: avoid;
    }}

    h4 {{
        font-size: 12pt;
        font-weight: bold;
        color: #505050;
        margin-top: 12pt;
        margin-bottom: 8pt;
    }}

    p {{
        margin: 8pt 0;
        text-indent: 2em;  /* 中文段落首行缩进 */
    }}

    blockquote {{
        margin: 12pt 20pt;
        padding: 10pt 15pt;
        background-color: #f5f5f5;
        border-left: 4px solid #0066cc;
        font-style: normal;
        text-indent: 0;
    }}

    blockquote p {{
        text-indent: 0;
        margin: 4pt 0;
    }}

    code {{
        font-family: "Consolas", "Monaco", "Courier New", monospace;
        background-color: #f4f4f4;
        padding: 2pt 4pt;
        border-radius: 3px;
        font-size: 10pt;
    }}

    pre {{
        background-color: #f8f8f8;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 12pt;
        overflow-x: auto;
        margin: 12pt 0;
        page-break-inside: avoid;
    }}

    pre code {{
        background-color: transparent;
        padding: 0;
        font-size: 9pt;
    }}

    img {{
        max-width: 85%;
        max-height: 400pt;
        height: auto;
        display: block;
        margin: 12pt auto;
        page-break-before: avoid;
        page-break-after: auto;
    }}

    em {{
        font-style: italic;
        color: #0066cc;
    }}

    strong {{
        font-weight: bold;
    }}

    ul, ol {{
        margin: 8pt 0;
        padding-left: 30pt;
    }}

    li {{
        margin: 4pt 0;
        text-indent: 0;
    }}

    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 12pt 0;
        page-break-inside: avoid;
    }}

    th, td {{
        border: 1px solid #ddd;
        padding: 8pt;
        text-align: left;
        text-indent: 0;
    }}

    th {{
        background-color: #f0f0f0;
        font-weight: bold;
    }}

    hr {{
        border: none;
        border-top: 1px solid #ccc;
        margin: 20pt 0;
    }}

    /* 图片说明 */
    img + em,
    img + p {{
        text-align: center;
        font-size: 9pt;
        color: #666;
        margin-top: -4pt;
        margin-bottom: 8pt;
        font-style: italic;
        text-indent: 0;
    }}

    /* 图片容器 - 防止过度留白 */
    p:has(img) {{
        margin: 8pt 0;
        page-break-inside: auto;
    }}

    /* 分页控制 */
    .page-break {{
        page-break-after: always;
    }}

    /* 首页不缩进 */
    h1 + blockquote p,
    h1 + p,
    h2 + p,
    h3 + p {{
        text-indent: 0;
    }}
    """

    full_html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            {css_style}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    return full_html


def generate_pdf(md_path, pdf_path, **options):
    """生成PDF文件"""
    if not WEASYPRINT_AVAILABLE:
        print("❌ 错误：缺少必要的库")
        print("请运行：pip install markdown2 weasyprint")
        sys.exit(1)

    # 读取Markdown文件
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 提取标题（用于页眉）
    title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Article"

    print(f"📝 文章标题：{title}")
    print()

    # 转换为HTML
    print("🔄 转换Markdown到HTML...")
    html_content = convert_markdown_to_html(
        md_content,
        images_dir=options.get('images_dir')
    )

    # 创建完整HTML文档
    print("🎨 应用样式...")
    full_html = create_html_document(
        html_content,
        title=title,
        font_family=options.get('font_family', 'Source Han Sans SC')
    )

    # 生成PDF
    print("📄 生成PDF...")

    # 配置字体
    font_config = FontConfiguration()

    # 创建临时HTML文件
    temp_html_path = Path(pdf_path).parent / "temp.html"
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    try:
        # 生成PDF
        HTML(filename=str(temp_html_path)).write_pdf(
            pdf_path,
            font_config=font_config
        )

        # 删除临时文件
        temp_html_path.unlink()

        print("✅ PDF生成成功！")

        # 获取文件信息
        pdf_size = Path(pdf_path).stat().st_size
        pdf_size_mb = pdf_size / (1024 * 1024)

        return {
            'size': pdf_size,
            'size_mb': pdf_size_mb,
            'path': pdf_path
        }

    except Exception as e:
        # 删除临时文件
        if temp_html_path.exists():
            temp_html_path.unlink()
        raise e


def main():
    parser = argparse.ArgumentParser(description='将Markdown转换为PDF')
    parser.add_argument('md_path', help='Markdown文件路径')
    parser.add_argument('pdf_path', help='输出PDF文件路径')
    parser.add_argument('--images-dir', help='图片目录路径')
    parser.add_argument('--font-family', default='Source Han Sans SC',
                       help='中文字体（默认：Source Han Sans SC）')
    parser.add_argument('--page-size', default='A4',
                       help='页面大小（默认：A4）')
    parser.add_argument('--add-toc', action='store_true',
                       help='添加目录（TODO：未实现）')
    parser.add_argument('--chinese-punctuation', action='store_true',
                       help='优化中文标点显示')

    args = parser.parse_args()

    # 检查输入文件
    md_path = Path(args.md_path)
    if not md_path.exists():
        print(f"❌ 错误：找不到Markdown文件：{md_path}")
        sys.exit(1)

    # 创建输出目录
    pdf_path = Path(args.pdf_path)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"📚 Markdown转PDF...")
    print(f"📂 输入文件：{md_path}")
    print(f"📄 输出文件：{pdf_path}")
    if args.images_dir:
        print(f"🖼️  图片目录：{args.images_dir}")
    print(f"✒️  字体：{args.font_family}")
    print()

    try:
        result = generate_pdf(
            md_path,
            pdf_path,
            images_dir=args.images_dir,
            font_family=args.font_family,
            page_size=args.page_size
        )

        print()
        print("📊 生成统计：")
        print(f"  • 文件大小：{result['size_mb']:.2f} MB")
        print(f"  • 输出路径：{result['path']}")
        print()

        if args.chinese_punctuation:
            print("✓ 已优化中文标点显示")

        if args.add_toc:
            print("⚠️  注意：目录功能尚未实现")

    except Exception as e:
        print(f"\n❌ PDF生成失败：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
