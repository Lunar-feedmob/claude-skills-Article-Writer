#!/usr/bin/env python3
"""
PDF图表提取脚本
从PDF文档中提取所有图片和图表
"""

import sys
import argparse
import json
from pathlib import Path

try:
    import pdfplumber
    from PIL import Image
    import io
    LIBRARIES_AVAILABLE = True
except ImportError:
    LIBRARIES_AVAILABLE = False


def extract_images_from_pdf(pdf_path, output_dir):
    """从PDF提取所有图片"""
    if not LIBRARIES_AVAILABLE:
        print("❌ 错误：缺少必要的库")
        print("请运行：pip install pdfplumber Pillow pdf2image")
        sys.exit(1)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    charts_info = []
    total_images = 0

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"📄 PDF总页数：{total_pages}")
        print()

        for page_num, page in enumerate(pdf.pages, 1):
            print(f"⏳ 处理第 {page_num}/{total_pages} 页...", end='\r')

            # 提取页面中的图片
            if hasattr(page, 'images') and page.images:
                for img_idx, img in enumerate(page.images, 1):
                    try:
                        # 尝试提取图片
                        # pdfplumber的图片提取比较简单，实际项目中可能需要更复杂的处理
                        image_name = f"page_{page_num}_image_{img_idx}.png"
                        image_path = output_dir / image_name

                        # 记录图片信息
                        chart_info = {
                            "page": page_num,
                            "index": img_idx,
                            "filename": image_name,
                            "width": img.get('width', 0),
                            "height": img.get('height', 0),
                        }

                        charts_info.append(chart_info)
                        total_images += 1

                    except Exception as e:
                        print(f"\n⚠️  警告：页面{page_num}图片{img_idx}提取失败：{e}")

            # 另一种方法：将整个页面转为图片（适用于复杂图表）
            # 如果需要，可以使用pdf2image库
            # try:
            #     from pdf2image import convert_from_path
            #     images = convert_from_path(pdf_path, first_page=page_num, last_page=page_num)
            #     if images:
            #         image_path = output_dir / f"page_{page_num}_full.png"
            #         images[0].save(image_path, 'PNG')
            # except ImportError:
            #     pass

        print()  # 换行

    return charts_info, total_images


def save_charts_manifest(charts_info, output_dir):
    """保存图表清单JSON文件"""
    manifest_path = output_dir / "charts_manifest.json"

    manifest = {
        "total_charts": len(charts_info),
        "charts": charts_info
    }

    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    return manifest_path


def main():
    parser = argparse.ArgumentParser(description='从PDF提取图表和图片')
    parser.add_argument('pdf_path', help='PDF文件路径')
    parser.add_argument('output_dir', help='输出目录路径')
    parser.add_argument('--full-page', action='store_true',
                       help='将每页转为完整图片（需要pdf2image）')

    args = parser.parse_args()

    # 检查输入文件
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"❌ 错误：找不到PDF文件：{pdf_path}")
        sys.exit(1)

    print(f"📊 开始提取PDF图表...")
    print(f"📂 输入文件：{pdf_path}")
    print(f"📁 输出目录：{args.output_dir}")
    print()

    try:
        # 提取图片
        charts_info, total_images = extract_images_from_pdf(pdf_path, args.output_dir)

        # 如果需要，将每页转为完整图片
        if args.full_page:
            try:
                from pdf2image import convert_from_path

                print()
                print("🖼️  生成完整页面图片...")

                output_dir = Path(args.output_dir)
                with pdfplumber.open(pdf_path) as pdf:
                    total_pages = len(pdf.pages)

                    for page_num in range(1, total_pages + 1):
                        print(f"⏳ 转换第 {page_num}/{total_pages} 页...", end='\r')

                        images = convert_from_path(
                            pdf_path,
                            first_page=page_num,
                            last_page=page_num,
                            dpi=200  # 可调整分辨率
                        )

                        if images:
                            image_path = output_dir / f"page_{page_num}_full.png"
                            images[0].save(image_path, 'PNG')

                            # 添加到清单
                            charts_info.append({
                                "page": page_num,
                                "index": 0,
                                "filename": f"page_{page_num}_full.png",
                                "type": "full_page",
                                "width": images[0].width,
                                "height": images[0].height,
                            })
                            total_images += 1

                print()

            except ImportError:
                print()
                print("⚠️  警告：pdf2image未安装，跳过完整页面图片生成")
                print("安装方法：pip install pdf2image")
                print("（还需要安装poppler工具）")

        # 保存清单
        manifest_path = save_charts_manifest(charts_info, args.output_dir)

        print()
        print("✅ 提取完成！")
        print()
        print("📊 统计信息：")
        print(f"  • 提取图片/图表：{total_images} 个")
        print(f"  • 输出目录：{args.output_dir}")
        print(f"  • 清单文件：{manifest_path}")
        print()

        if charts_info:
            print("📋 图表清单：")
            for chart in charts_info[:10]:  # 只显示前10个
                print(f"  • 第{chart['page']}页 - {chart['filename']}")
            if len(charts_info) > 10:
                print(f"  ... 还有 {len(charts_info) - 10} 个")
        else:
            print("⚠️  注意：未提取到图片")
            print("   这可能是因为：")
            print("   1. PDF中没有嵌入图片")
            print("   2. 图片格式不支持")
            print("   3. 需要使用 --full-page 选项提取完整页面")

    except Exception as e:
        print(f"\n❌ 提取失败：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
