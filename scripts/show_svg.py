"""Do not use this as the delivered figure.

The reply must contain a PNG. Opening the SVG is not the result.
"""

from __future__ import annotations

import sys


def main() -> int:
    print("不要打开 SVG 当作成品。先把 SVG 转成 PNG，确认中文还在，再把 PNG 放进回复。")
    return 2


if __name__ == "__main__":
    sys.exit(main())
