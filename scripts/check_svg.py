"""Check that a study figure is a self-contained, labeled SVG.

Python 3 standard library only. Exit 0 when the file passes.
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET

BANNED_TAGS = {
    "script",
    "foreignObject",
    "iframe",
    "embed",
    "object",
    "image",
    "audio",
    "video",
}
SHAPE_TAGS = {"path", "line", "polyline", "polygon", "circle", "rect", "ellipse"}
LINK_ATTRS = {"href", "{http://www.w3.org/1999/xlink}href"}


def local_name(tag: str) -> str:
    if tag.startswith("{"):
        return tag.rsplit("}", 1)[1]
    return tag


def check(path: str, required_text: list[str]) -> list[str]:
    errors: list[str] = []
    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        return [f"XML 解析失败: {exc}"]

    root = tree.getroot()
    if local_name(root.tag) != "svg":
        errors.append("根节点必须是 svg")

    view_box = root.get("viewBox")
    if not view_box:
        errors.append("缺少 viewBox")
    else:
        parts = view_box.replace(",", " ").split()
        if len(parts) != 4:
            errors.append(f"viewBox 必须是 4 个数，当前是 {view_box!r}")
        else:
            try:
                nums = [float(part) for part in parts]
            except ValueError:
                errors.append(f"viewBox 含有非数字: {view_box!r}")
            else:
                if nums[2] <= 0 or nums[3] <= 0:
                    errors.append("viewBox 的宽高必须为正")

    saw_shape = False
    for element in root.iter():
        name = local_name(element.tag)
        if name in BANNED_TAGS:
            errors.append(f"不允许的标签 <{name}>，示意图必须自包含")
        if name in SHAPE_TAGS:
            saw_shape = True
        for attr, value in element.attrib.items():
            attr_name = local_name(attr)
            if attr_name.lower().startswith("on"):
                errors.append(f"不允许事件属性 {attr_name}")
            if attr in LINK_ATTRS or attr_name == "href":
                if str(value).startswith(("http://", "https://", "//")):
                    errors.append(f"不允许外部链接 {value}")

    if not saw_shape:
        errors.append("没有 path/line/circle/rect 等图形，只有文字不算示意图")

    text = "".join(root.itertext())
    for item in required_text:
        if item not in text:
            errors.append(f"图中缺少标注 {item}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="检查学习示意图 SVG")
    parser.add_argument("svg", help="SVG 文件路径")
    parser.add_argument(
        "--require-text",
        action="append",
        default=[],
        help="图中必须出现的标注，可重复传入",
    )
    args = parser.parse_args()
    errors = check(args.svg, args.require_text)
    if errors:
        print(f"FAIL {args.svg}")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"OK {args.svg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
