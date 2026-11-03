"""Run the SVG checker against the bundled examples."""

from __future__ import annotations

import sys
from pathlib import Path

from check_svg import check

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"

CASES = [
    (
        "ionosphere-right-triangle.svg",
        ["地心", "发射点", "反射点", "直角", "(R+h)", "2Rh", "弧长", "已夸大"],
    ),
    (
        "cosine-waveform.svg",
        ["v(t)", "A cos", "T"],
    ),
    (
        "am-block.svg",
        ["m(t)", "c(t)", "s(t)", "相乘"],
    ),
    (
        "resistor-divider.svg",
        ["R₁", "R₂", "Vin", "Vo"],
    ),
    (
        "am-waveform.svg",
        ["s(t)", "f_m", "f_c"],
    ),
    (
        "am-spectrum.svg",
        ["0.25", "f_c−f_m", "f_c+f_m"],
    ),
    (
        "sampling-time.svg",
        ["Ts", "x(t)"],
    ),
    (
        "sampling-spectrum.svg",
        ["1/Ts", "幅度"],
    ),
    (
        "line-of-sight.svg",
        ["切点", "ht", "hr", "4.12", "6371"],
    ),
    (
        "dsb-sc-spectrum.svg",
        ["无载波", "f_c−f_m", "f_c+f_m"],
    ),
    (
        "dsb-sc-block.svg",
        ["相乘", "m(t)", "没有加直流"],
    ),
    (
        "phone-sampling.svg",
        ["3.4", "8", "不混叠"],
    ),
]


def main() -> int:
    failed = False
    for name, required in CASES:
        path = EXAMPLES / name
        errors = check(str(path), required)
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"- {error}")
        else:
            print(f"OK {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
