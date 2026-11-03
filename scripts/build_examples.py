"""Rebuild the four bundled example figures.

This script only regenerates files in examples/. Study questions are answered
by writing a new SVG, not by running this file.
"""

from __future__ import annotations

import math
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "examples"

INK = "#0f172a"
BLUE = "#0b57d0"
ORANGE = "#c2410c"
MUTED = "#64748b"
HAIR = "#94a3b8"
CARD = "#f8fafc"
LINE = "#e2e8f0"
FONT = "Microsoft YaHei, SimHei, Noto Sans CJK SC, sans-serif"


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def text(
    x: float,
    y: float,
    content: str,
    size: float = 16,
    fill: str = INK,
    anchor: str = "start",
    weight: int = 400,
    halo: bool = False,
) -> str:
    stroke = ' stroke="#ffffff" stroke-width="5" paint-order="stroke fill" stroke-linejoin="round"' if halo else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}"{stroke}>{esc(content)}</text>'
    )


def document(view_box: str, title: str, desc: str, body: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}" font-family="{FONT}">
  <title>{esc(title)}</title>
  <desc>{esc(desc)}</desc>
  <rect width="100%" height="100%" fill="#ffffff"/>
  {body}
</svg>
'''


def arrow_defs(color: str = INK) -> str:
    return f'''<defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/>
    </marker>
  </defs>'''


def ionosphere() -> str:
    r_km = 6371.0
    h_km = 300.0
    x_km = math.sqrt((r_km + h_km) ** 2 - r_km**2)
    x_approx = math.sqrt(2 * r_km * h_km)
    theta = math.atan(x_km / r_km)
    arc_km = r_km * theta
    pct = 100.0 * h_km / (2 * r_km)

    cx, cy = 250.0, 470.0
    radius = 200.0
    tangent = 188.0
    tx, ty = cx, cy - radius
    px, py = tx - tangent, ty
    cpx = px - cx
    cpy = py - cy
    cp_len = math.hypot(cpx, cpy)
    sx = cx + radius * cpx / cp_len
    sy = cy + radius * cpy / cp_len
    assert abs((cx - tx) * (px - tx) + (cy - ty) * (py - ty)) < 1e-6

    def polar(deg: float, rad: float) -> tuple[float, float]:
        ang = math.radians(deg)
        return (cx - rad * math.sin(ang), cy - rad * math.cos(ang))

    arc_start = polar(-32, radius)
    arc_end = polar(118, radius)
    mid_ang = math.atan2(cx - sx, cy - sy) * 0.55
    arc_x = cx - radius * math.sin(mid_ang)
    arc_y = cy - radius * math.cos(mid_ang)
    label_x = arc_x + (cx - arc_x) / radius * 34
    label_y = arc_y + (cy - arc_y) / radius * 34

    parts = [
        arrow_defs(),
        text(36, 42, "电离层反射的直角三角形", 22, weight=700),
        text(36, 70, "h 已夸大。直角在发射点：半径垂直于切线。", 14, MUTED),
        (
            f'<path d="M {arc_start[0]:.1f} {arc_start[1]:.1f} '
            f'A {radius:.1f} {radius:.1f} 0 0 0 {arc_end[0]:.1f} {arc_end[1]:.1f}" '
            f'fill="none" stroke="{INK}" stroke-width="2.5"/>'
        ),
        (
            f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{px:.1f}" y2="{py:.1f}" '
            f'stroke="{INK}" stroke-width="2"/>'
        ),
        (
            f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{px:.1f}" y2="{py:.1f}" '
            f'stroke="{ORANGE}" stroke-width="4" stroke-linecap="round"/>'
        ),
        (
            f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" '
            f'stroke="{INK}" stroke-width="2.5"/>'
        ),
        (
            f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" '
            f'stroke="{BLUE}" stroke-width="3"/>'
        ),
        text(label_x, label_y, "弧长", 14, MUTED, "middle", halo=True),
        (
            f'<path d="M {tx - 16:.1f} {ty:.1f} L {tx - 16:.1f} {ty + 16:.1f} '
            f'L {tx:.1f} {ty + 16:.1f}" fill="none" stroke="{INK}" stroke-width="1.8"/>'
        ),
        text(tx + 8, ty + 36, "直角", 13, halo=True),
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="{INK}"/>',
        f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="4.5" fill="{INK}"/>',
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="{ORANGE}"/>',
        f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="3.5" fill="{INK}"/>',
        text(cx, cy + 28, "地心", 16, anchor="middle", halo=True),
        text(tx + 12, ty - 12, "发射点", 16, halo=True),
        text(px, py - 16, "反射点", 16, anchor="middle", halo=True),
        text(tx + 14, (ty + cy) / 2 + 6, "R", 18, weight=700, halo=True),
        text((px + tx) / 2, ty - 14, "x", 18, BLUE, "middle", 700, True),
        text((cx + px) / 2 - 28, (cy + py) / 2 + 22, "R+h", 18, weight=700, halo=True),
        text((sx + px) / 2 - 22, (sy + py) / 2 + 6, "h", 18, ORANGE, "middle", 700, True),
        (
            f'<path d="M {tx:.1f} {ty:.1f} A {radius:.1f} {radius:.1f} 0 0 0 {sx:.1f} {sy:.1f}" '
            f'fill="none" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 4"/>'
        ),
        '<rect x="520" y="104" width="400" height="470" rx="14" fill="#f8fafc" stroke="#e2e8f0"/>',
        text(544, 146, "勾股关系", 20, weight=700),
        text(544, 196, "(R+h)² = R² + x²", 18),
        (
            '<text x="544" y="234" font-size="18" fill="#0f172a">'
            "x² = 2Rh + "
            '<tspan fill="#c2410c">h²</tspan></text>'
        ),
        text(544, 278, "h ≪ 2R 时可以略去 h²", 16),
        text(544, 312, "x ≈ √(2Rh)", 18, BLUE, weight=700),
        '<line x1="544" y1="340" x2="880" y2="340" stroke="#e2e8f0"/>',
        text(544, 376, "R = 6371 km，h = 300 km", 16),
        text(544, 410, f"h² / 2Rh = {pct:.1f}%", 16, ORANGE),
        text(544, 444, f"切线 x = {x_km:.0f} km", 16, BLUE),
        text(544, 478, f"略去 h² 后 x ≈ {x_approx:.0f} km", 16),
        text(544, 512, f"地面弧长 = {arc_km:.0f} km", 16),
        text(544, 550, "x 是切线。h ≪ R 时才把它当成单程地面距离。", 13, MUTED),
    ]
    desc = (
        "地心、发射点、电离层反射点构成直角三角形。"
        f"切线 x = {x_km:.0f} km，地面弧长 = {arc_km:.0f} km。h 已夸大。"
    )
    return document("0 0 960 640", "电离层反射的直角三角形模型", desc, "\n  ".join(parts))


def waveform() -> str:
    x0, x1 = 190.0, 560.0
    axis_x = 120.0
    mid, amp = 250.0, 88.0
    points = []
    for i in range(121):
        t = i / 120
        x = x0 + (x1 - x0) * t
        y = mid - amp * math.cos(2 * math.pi * t)
        points.append(f"{x:.1f},{y:.1f}")
    peak_y = mid - amp
    parts = [
        arrow_defs(),
        text(36, 38, "余弦信号", 22, weight=700),
        text(176, 38, "v(t) = A cos(2πt / T)", 18, BLUE),
        f'<line x1="{axis_x}" y1="{mid}" x2="{axis_x}" y2="72" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        f'<line x1="{axis_x}" y1="{mid}" x2="680" y2="{mid}" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        text(axis_x - 12, 84, "v(t)", 15, anchor="end"),
        text(694, mid + 5, "t", 15),
        text(axis_x - 12, mid + 18, "0", 14, MUTED, "end"),
        f'<polyline points="{" ".join(points)}" fill="none" stroke="{BLUE}" stroke-width="2.6"/>',
        f'<line x1="156" y1="{mid}" x2="156" y2="{peak_y}" stroke="{INK}" stroke-width="1.4" marker-start="url(#arrow)" marker-end="url(#arrow)"/>',
        text(142, (mid + peak_y) / 2 + 5, "A", 18, anchor="end", weight=700, halo=True),
        f'<line x1="{x0}" y1="{mid + 34}" x2="{x1}" y2="{mid + 34}" stroke="{INK}" stroke-width="1.4" marker-start="url(#arrow)" marker-end="url(#arrow)"/>',
        f'<line x1="{x0}" y1="{mid}" x2="{x0}" y2="{mid + 40}" stroke="{HAIR}" stroke-width="1.2"/>',
        f'<line x1="{x1}" y1="{mid}" x2="{x1}" y2="{mid + 40}" stroke="{HAIR}" stroke-width="1.2"/>',
        text((x0 + x1) / 2, mid + 58, "T", 18, anchor="middle", weight=700),
    ]
    desc = "一个周期的余弦信号 v(t) = A cos(2πt / T)，标出幅值 A 和周期 T。"
    return document("0 0 760 400", "余弦信号", desc, "\n  ".join(parts))


def block() -> str:
    parts = [
        arrow_defs(),
        text(40, 44, "幅度调制", 22, weight=700),
        text(168, 44, "s(t) = [A + m(t)] c(t)", 18, BLUE),
        '<rect x="210" y="130" width="150" height="72" rx="8" fill="#ffffff" stroke="#0f172a" stroke-width="1.8"/>',
        '<rect x="430" y="130" width="150" height="72" rx="8" fill="#ffffff" stroke="#0f172a" stroke-width="1.8"/>',
        text(285, 172, "加直流 A", 16, anchor="middle"),
        text(505, 172, "相乘", 16, anchor="middle"),
        f'<line x1="40" y1="166" x2="210" y2="166" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        f'<line x1="360" y1="166" x2="430" y2="166" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        f'<line x1="580" y1="166" x2="730" y2="166" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        f'<line x1="505" y1="280" x2="505" y2="202" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        text(118, 150, "m(t)", 16, BLUE, "middle", 700, True),
        text(392, 150, "A+m(t)", 15, anchor="middle", halo=True),
        text(655, 150, "s(t)", 16, BLUE, "middle", 700, True),
        text(468, 268, "c(t)", 16, BLUE, "end", 700, True),
        text(40, 320, "c(t) = cos(2π f_c t)。A 是载波幅度里的直流项。", 15, MUTED),
    ]
    desc = "幅度调制框图：消息先加直流 A，再与载波 c(t) 相乘，得到 s(t)。"
    return document("0 0 780 360", "幅度调制框图", desc, "\n  ".join(parts))


def divider() -> str:
    top, bot = 120.0, 300.0
    src, node = 120.0, 430.0
    parts = [
        text(40, 44, "串联分压", 22, weight=700),
        text(168, 44, "Vo = Vin · R₂ / (R₁ + R₂)", 18, BLUE),
        f'<line x1="{src}" y1="{top}" x2="250" y2="{top}" stroke="{INK}" stroke-width="1.8"/>',
        f'<rect x="250" y="{top - 14}" width="110" height="28" fill="#ffffff" stroke="{INK}" stroke-width="1.8"/>',
        f'<line x1="360" y1="{top}" x2="{node}" y2="{top}" stroke="{INK}" stroke-width="1.8"/>',
        text(305, top - 24, "R₁", 18, anchor="middle", weight=700),
        f'<line x1="{node}" y1="{top}" x2="{node}" y2="176" stroke="{INK}" stroke-width="1.8"/>',
        f'<rect x="{node - 14}" y="176" width="28" height="78" fill="#ffffff" stroke="{INK}" stroke-width="1.8"/>',
        f'<line x1="{node}" y1="254" x2="{node}" y2="{bot}" stroke="{INK}" stroke-width="1.8"/>',
        text(node + 28, 224, "R₂", 18, weight=700),
        f'<line x1="{src}" y1="{top}" x2="{src}" y2="168" stroke="{INK}" stroke-width="1.8"/>',
        f'<circle cx="{src}" cy="210" r="28" fill="#ffffff" stroke="{INK}" stroke-width="1.8"/>',
        text(src, 204, "+", 16, anchor="middle"),
        text(src, 226, "−", 16, anchor="middle"),
        f'<line x1="{src}" y1="238" x2="{src}" y2="{bot}" stroke="{INK}" stroke-width="1.8"/>',
        f'<line x1="{src}" y1="{bot}" x2="{node}" y2="{bot}" stroke="{INK}" stroke-width="1.8"/>',
        f'<line x1="{node}" y1="{bot}" x2="{node}" y2="318" stroke="{INK}" stroke-width="1.8"/>',
        f'<line x1="{node - 18}" y1="318" x2="{node + 18}" y2="318" stroke="{INK}" stroke-width="1.8"/>',
        f'<line x1="{node - 11}" y1="326" x2="{node + 11}" y2="326" stroke="{INK}" stroke-width="1.8"/>',
        f'<line x1="{node - 5}" y1="334" x2="{node + 5}" y2="334" stroke="{INK}" stroke-width="1.8"/>',
        f'<circle cx="{node}" cy="{top}" r="3.5" fill="{INK}"/>',
        text(src - 18, 214, "Vin", 16, anchor="end", weight=700, halo=True),
        text(node + 14, top - 16, "Vo", 16, BLUE, weight=700, halo=True),
        text(40, 390, "电流从 Vin 正极经 R₁、R₂ 回到负极。Vo 取在 R₂ 两端。", 15, MUTED),
    ]
    desc = "两个电阻串联分压。Vo = Vin · R₂ / (R₁ + R₂)，Vo 是 R₂ 两端电压。"
    return document("0 0 760 430", "串联分压", desc, "\n  ".join(parts))


def am_waveform() -> str:
    x0, x1 = 80.0, 700.0
    mid, scale = 220.0, 64.0
    carrier, upper, lower = [], [], []
    for i in range(721):
        t = i / 720
        x = x0 + (x1 - x0) * t
        env = 1 + 0.5 * math.cos(2 * math.pi * t)
        carrier.append(f"{x:.1f},{mid - scale * env * math.cos(24 * math.pi * t):.1f}")
        upper.append(f"{x:.1f},{mid - scale * env:.1f}")
        lower.append(f"{x:.1f},{mid + scale * env:.1f}")
    parts = [
        arrow_defs(),
        text(36, 36, "单音幅度调制", 22, weight=700),
        text(36, 64, "s(t) = [1 + 0.5 cos(2π f_m t)] cos(2π f_c t)", 15, BLUE),
        f'<line x1="48" y1="{mid}" x2="48" y2="78" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        f'<line x1="48" y1="{mid}" x2="730" y2="{mid}" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        text(36, 92, "s(t)", 14, anchor="end"),
        text(736, mid + 6, "t", 15),
        f'<polyline points="{" ".join(upper)}" fill="none" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="7 4"/>',
        f'<polyline points="{" ".join(lower)}" fill="none" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="7 4"/>',
        f'<polyline points="{" ".join(carrier)}" fill="none" stroke="{BLUE}" stroke-width="1.6"/>',
        text(470, 108, "+[1 + 0.5 cos(2π f_m t)]", 14, ORANGE, halo=True),
        text(210, 372, "−[1 + 0.5 cos(2π f_m t)]", 14, ORANGE, halo=True),
    ]
    desc = "调幅时域。载波在包络内振荡，包络不穿过横轴。"
    return document("0 0 760 420", "单音幅度调制时域", desc, "\n  ".join(parts))


def am_spectrum() -> str:
    base = 300.0
    heights = {"0.25": 50.0, "1": 200.0}
    stems = [(150, "0.25", "f_c−f_m"), (340, "1", "f_c"), (530, "0.25", "f_c+f_m")]
    parts = [
        arrow_defs(),
        text(36, 40, "单音幅度调制频谱", 22, weight=700),
        f'<line x1="70" y1="{base}" x2="70" y2="48" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        f'<line x1="70" y1="{base}" x2="700" y2="{base}" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        text(58, 56, "幅度", 14, anchor="end"),
        text(712, base + 6, "f", 15),
    ]
    for x, height, freq in stems:
        y = base - heights[height]
        parts.append(
            f'<line x1="{x}" y1="{base}" x2="{x}" y2="{y}" stroke="{BLUE}" stroke-width="2.4"/>'
        )
        parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{BLUE}"/>')
        parts.append(text(x, y - 12, height, 16, BLUE, "middle", 700, True))
        parts.append(text(x, base + 28, freq, 15, anchor="middle"))
    desc = "正频率频谱。载波高度 1，两侧边频高度 0.25。"
    return document("0 0 760 380", "单音幅度调制频谱", desc, "\n  ".join(parts))


def sampling() -> str:
    base = 250.0
    xs = [120, 230, 340, 450, 560]
    amps = [70, 110, 40, -80, -30]
    parts = [
        arrow_defs(),
        text(36, 40, "冲激抽样", 22, weight=700),
        f'<line x1="70" y1="{base}" x2="70" y2="70" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        f'<line x1="70" y1="{base}" x2="680" y2="{base}" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        text(52, 78, "x(t)", 14, anchor="end"),
        text(692, base + 6, "t", 15),
    ]
    for x, amp in zip(xs, amps):
        y = base - amp
        parts.append(f'<line x1="{x}" y1="{base}" x2="{x}" y2="{y}" stroke="{BLUE}" stroke-width="2"/>')
        parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{BLUE}"/>')
    parts.append(
        f'<line x1="{xs[0]}" y1="{base + 36}" x2="{xs[1]}" y2="{base + 36}" stroke="{INK}" stroke-width="1.4" marker-start="url(#arrow)" marker-end="url(#arrow)"/>'
    )
    parts.append(text((xs[0] + xs[1]) / 2, base + 58, "Ts", 18, anchor="middle", weight=700))
    parts.append(text(36, 400, "相邻冲激的间隔是 Ts，不是 1/Ts。", 15, MUTED))
    desc = "冲激抽样的时域。相邻冲激间隔标为 Ts。"
    return document("0 0 740 430", "冲激抽样", desc, "\n  ".join(parts))


def sampling_spectrum() -> str:
    base = 250.0
    stems = [(180, "−1/Ts"), (360, "0"), (540, "1/Ts")]
    parts = [
        arrow_defs(),
        text(36, 40, "抽样冲激串的频谱", 22, weight=700),
        f'<line x1="70" y1="{base}" x2="70" y2="70" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        f'<line x1="70" y1="{base}" x2="680" y2="{base}" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        text(52, 78, "幅度", 14, anchor="end"),
        text(692, base + 6, "f", 15),
    ]
    for x, label in stems:
        parts.append(f'<line x1="{x}" y1="{base}" x2="{x}" y2="110" stroke="{BLUE}" stroke-width="2.4"/>')
        parts.append(f'<circle cx="{x}" cy="110" r="4" fill="{BLUE}"/>')
        parts.append(text(x, base + 28, label, 16, anchor="middle"))
    parts.append(
        f'<line x1="360" y1="{base + 62}" x2="540" y2="{base + 62}" stroke="{INK}" stroke-width="1.4" marker-start="url(#arrow)" marker-end="url(#arrow)"/>'
    )
    parts.append(text(450, base + 84, "1/Ts", 18, anchor="middle", weight=700))
    desc = "抽样冲激串的频谱，三根线一样高。已抽样信号的频谱不是这三根线，而要复制原信号的形状。"
    return document("0 0 740 380", "抽样频谱", desc, "\n  ".join(parts))


def dsb_sc_block() -> str:
    parts = [
        arrow_defs(),
        text(36, 42, "抑制载波", 22, weight=700),
        text(168, 42, "s(t) = m(t) c(t)", 18, BLUE),
        '<rect x="280" y="130" width="160" height="72" rx="8" fill="#ffffff" stroke="#0f172a" stroke-width="1.8"/>',
        text(360, 172, "相乘", 16, anchor="middle"),
        f'<line x1="40" y1="166" x2="280" y2="166" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        f'<line x1="440" y1="166" x2="660" y2="166" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        f'<line x1="360" y1="280" x2="360" y2="202" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        text(150, 150, "m(t)", 16, BLUE, "middle", 700, True),
        text(540, 150, "s(t)", 16, BLUE, "middle", 700, True),
        text(330, 268, "c(t)", 16, BLUE, "end", 700, True),
        text(36, 330, "没有加直流。c(t) = cos(2π f_c t)。", 15, MUTED),
    ]
    desc = "抑制载波框图。只有相乘，没有加直流。"
    return document("0 0 720 370", "抑制载波框图", desc, "\n  ".join(parts))


def line_of_sight() -> str:
    cx, cy, radius = 430.0, 430.0, 210.0
    gx, gy = cx, cy - radius
    left, right = 160.0, 80.0
    ax, ay = gx - left, gy
    bx, by = gx + right, gy
    oa = math.hypot(ax - cx, ay - cy)
    ob = math.hypot(bx - cx, by - cy)
    sax = cx + radius * (ax - cx) / oa
    say = cy + radius * (ay - cy) / oa
    sbx = cx + radius * (bx - cx) / ob
    sby = cy + radius * (by - cy) / ob
    arc0 = (cx - radius * math.sin(math.radians(-50)), cy - radius * math.cos(math.radians(-50)))
    arc1 = (cx - radius * math.sin(math.radians(70)), cy - radius * math.cos(math.radians(70)))
    parts = [
        text(36, 40, "两天线视距", 22, weight=700),
        text(36, 66, "直角在地面切点，不在天线处。高度已夸大。", 14, MUTED),
        (
            f'<path d="M {arc0[0]:.1f} {arc0[1]:.1f} A {radius:.1f} {radius:.1f} 0 0 0 '
            f'{arc1[0]:.1f} {arc1[1]:.1f}" fill="none" stroke="{INK}" stroke-width="2.4"/>'
        ),
        f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{gx:.1f}" y2="{gy:.1f}" stroke="{INK}" stroke-width="2"/>',
        f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{BLUE}" stroke-width="2.4"/>',
        f'<line x1="{sax:.1f}" y1="{say:.1f}" x2="{ax:.1f}" y2="{ay:.1f}" stroke="{ORANGE}" stroke-width="3"/>',
        f'<line x1="{sbx:.1f}" y1="{sby:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{ORANGE}" stroke-width="3"/>',
        f'<path d="M {gx-14:.1f} {gy:.1f} L {gx-14:.1f} {gy+14:.1f} L {gx:.1f} {gy+14:.1f}" fill="none" stroke="{INK}" stroke-width="1.6"/>',
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="{INK}"/>',
        f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="4" fill="{INK}"/>',
        f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="4" fill="{ORANGE}"/>',
        f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="4" fill="{ORANGE}"/>',
        text(cx, cy + 24, "地心", 15, anchor="middle", halo=True),
        text(gx + 10, gy + 46, "切点", 15, halo=True),
        text(ax, ay - 46, "发射天线", 15, anchor="middle", halo=True),
        text(bx, by - 46, "接收天线", 15, anchor="middle", halo=True),
        text(cx + 12, (cy + gy) / 2, "R", 16, weight=700, halo=True),
        text((ax + gx) / 2, gy - 18, "x₁", 16, BLUE, "middle", 700, True),
        text((bx + gx) / 2, gy - 18, "x₂", 16, BLUE, "middle", 700, True),
        text(ax - 8, (say + ay) / 2, "ht", 15, ORANGE, "end", halo=True),
        text(bx + 10, (sby + by) / 2, "hr", 15, ORANGE, halo=True),
        text(36, 500, "ht = 100 m，hr = 25 m 时，d = 4.12(√ht + √hr) = 61.8 km。", 15),
        text(36, 528, "4.12 用的是等效地球半径 4R/3。改用 R = 6371 km 会得到约 53.6 km。", 14, MUTED),
    ]
    desc = "两座天线的视距。直角在地面切点。ht、hr 为天线高度，已夸大。"
    return document("0 0 820 620", "两天线视距", desc, "\n  ".join(parts))


def dsb_sc_spectrum() -> str:
    base = 280.0
    stems = [(220, 90.0, "Ac/2", "f_c−f_m"), (520, 90.0, "Ac/2", "f_c+f_m")]
    parts = [
        arrow_defs(),
        text(36, 40, "抑制载波双边带", 22, weight=700),
        text(36, 68, "s(t) = Ac cos(2π f_m t) cos(2π f_c t)", 16, BLUE),
        f'<line x1="80" y1="{base}" x2="80" y2="96" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        f'<line x1="80" y1="{base}" x2="700" y2="{base}" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        text(64, 104, "幅度", 14, anchor="end"),
        text(712, base + 6, "f", 15),
        text(370, base + 28, "f_c", 16, MUTED, "middle"),
        text(370, base - 18, "无载波", 15, ORANGE, "middle", halo=True),
    ]
    for x, height, amp, freq in stems:
        y = base - height
        parts.append(f'<line x1="{x}" y1="{base}" x2="{x}" y2="{y}" stroke="{BLUE}" stroke-width="2.4"/>')
        parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{BLUE}"/>')
        parts.append(text(x, y - 14, amp, 16, BLUE, "middle", 700, True))
        parts.append(text(x, base + 28, freq, 15, anchor="middle"))
    desc = "DSB-SC 频谱。只有两条边频，fc 处没有谱线。"
    return document("0 0 760 360", "抑制载波双边带频谱", desc, "\n  ".join(parts))


def phone_sampling() -> str:
    base = 250.0
    parts = [
        arrow_defs(),
        text(36, 36, "话带抽样频谱", 22, weight=700),
        text(36, 62, "f_H = 3.4 kHz，f_s = 8 kHz", 15, BLUE),
        f'<line x1="60" y1="{base}" x2="60" y2="84" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        f'<line x1="60" y1="{base}" x2="800" y2="{base}" stroke="{INK}" stroke-width="1.8" marker-end="url(#arrow)"/>',
        text(48, 92, "幅度", 14, anchor="end"),
        text(812, base + 4, "f", 15),
        '<polygon points="300,250 392,170 484,250" fill="none" stroke="#0b57d0" stroke-width="2"/>',
        '<polygon points="520,250 612,170 704,250" fill="none" stroke="#0b57d0" stroke-width="2"/>',
        text(392, base + 24, "0", 14, anchor="middle"),
        text(300, base + 24, "−3.4", 13, anchor="middle"),
        text(484, base + 24, "3.4", 13, anchor="middle"),
        text(612, base + 24, "8", 14, BLUE, "middle", 700),
        text(392, 150, "基带", 14, BLUE, "middle"),
        text(720, 150, "复制", 14, BLUE, "start"),
        text(502, 210, "空隙", 14, ORANGE, "middle"),
        text(36, 320, "间隔 f_s = 8 kHz。每份宽度 2f_H = 6.8 kHz。8 > 6.8，所以不混叠。", 15),
    ]
    desc = "话带信号抽样频谱。f_H = 3.4 kHz，f_s = 8 kHz，复制谱之间有空隙。"
    return document("0 0 860 360", "话带抽样频谱", desc, "\n  ".join(parts))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    files = {
        "ionosphere-right-triangle.svg": ionosphere(),
        "cosine-waveform.svg": waveform(),
        "am-block.svg": block(),
        "resistor-divider.svg": divider(),
        "am-waveform.svg": am_waveform(),
        "am-spectrum.svg": am_spectrum(),
        "sampling-time.svg": sampling(),
        "sampling-spectrum.svg": sampling_spectrum(),
        "line-of-sight.svg": line_of_sight(),
        "dsb-sc-spectrum.svg": dsb_sc_spectrum(),
        "dsb-sc-block.svg": dsb_sc_block(),
        "phone-sampling.svg": phone_sampling(),
    }
    for name, content in files.items():
        path = OUT / name
        path.write_text(content, encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
