---
name: ee-study-figure
description: >-
  Draws a visible labeled study figure on the first reply for
  electronic-information coursework. The first message must already contain
  the opened picture, not a text-only explanation. Covers geometry models
  (电离层, 视距, 反射), waveforms and spectra, system block diagrams, and
  basic circuit schematics. Use when the user pastes 豆包, Doubao, DeepSeek,
  or textbook prose, asks for 示意图, 波形, 频谱, 框图, 电路图, or brings an
  ASCII diagram that is hard to read.
---

# 电子信息学习示意图

把讲解、公式或文字示意图画成一张用户能直接看见的图。图上的点、线段和公式必须是同一套关系。默认中文标注。

第一次回复里就必须有图。动手顺序只有这一条：写 SVG，立刻转成 PNG，把 PNG 放进回复，再在图下面写 4 到 8 行说明。不要先把 SVG 交给用户。禁止先发一段只有文字的回复，禁止等用户再说「出图」才画。第一次如果只有文字、代码或「绘制说明」，这次任务失败。

照片、PCB、器件实物不在这个技能里。用户要这类图时，改问清要表达的公式或结构，再画对应的示意图。

用户指出「有人把这些点画在一条直线上」时，那句话描述的是错误画法。按等式把图画对，不要把等式本身改判成另一个模型，也不要先写一篇纠错说明来代替图。

## 先定轴，再画

动笔前先写清两根轴，写在图下面，不能单独占掉第一次回复：

- 横轴：物理量、符号、单位，以及必须标出的点
- 纵轴：物理量、符号、单位，以及必须标出的高度或幅度

波形和频谱必须有这两根轴。几何图里，横轴和纵轴就是两条直角边：写明哪一条边水平、哪一条边竖直、直角在哪个点。框图从左到右是信号流向，不设坐标轴。电路按节点和极性画，不设坐标轴。

轴没定下来就不要画。定下来之后，图上的箭头、刻度和符号必须和这两行一致。

关系接着写在轴的下面，每行一句：

1. 顶点，以及直角或参考方向在哪个点
2. 每条边、箭头或端口对应的符号
3. 这张图必须满足的等式

文字示意图和等式冲突时，以等式为准，并说明文字示意图错在哪。

等式 (R+h)² = R² + x² 表示直角在发射点：R 沿半径，x 沿切线，二者垂直，R+h 是斜边。地心、发射点、反射点不共线。禁止写成「三点共线，再把 x 当成直角边」。

## 字要写在图上

每个点的名字、每条边的符号，都用文字贴在对应的点或线段旁边。盖住旁边的公式卡片之后，图仍然能单独看懂。只在卡片或正文里解释、图上不写字，这张图不合格。

电离层这张图上必须能直接读到：地心、发射点、反射点、直角、R、x、R+h、h、弧长。检查时这些词都要传给 `--require-text`。

## 选一种图

| 用户在讲 | 类型 | 图上必须出现 |
| --- | --- | --- |
| 距离、高度、反射、视距、直角三角形 | geometry | 直角标记、各边符号、被讨论是否略去的项 |
| 时域波形、频谱、抽样、调制波形 | waveform | 坐标轴名称、幅值、周期或频率 |
| 发射机、接收机、锁相环、处理流程 | block | 从左到右的方框和信号名 |
| 电阻、电容、电源、分压、KVL | circuit | 符号、极性、电压或电流方向 |

一次只画承担这条等式的那一张。另一种关系在这张图上看不见时，再另存一张 SVG。

## 输出

第一次回复的成品必须是 PNG。只贴 LaTeX、TikZ、Mermaid 或 SVG 源码，任务失败，这些格式一律不要写进回复。不要先交 SVG，再在下一轮改成 PNG。

- 先把图写到 `figures/<英文短名>.svg`。已有同名文件就换短名，不覆盖
- 写完立刻转成同名 PNG，回复里只放这张 PNG
- 转 PNG 时字体用 `Microsoft YaHei, SimHei, Noto Sans CJK SC, sans-serif`。转完先看 PNG：中文点名还在，才发出去；字丢了就换字体重转，不要把缺字的图交出去
- 再用 4 到 8 行说明每个符号、等式、近似成立的条件
- 然后运行检查脚本。脚本和本文件在同一目录：

```bash
python "<本 SKILL.md 所在目录>/scripts/check_svg.py" "figures/<英文短名>.svg" --require-text "<符号1>" --require-text "<符号2>"
```

`--require-text` 至少覆盖等式里的每个独立符号，以及图题里的关键点名。检查失败就改 SVG，通过后再交给用户。机器上没有 Python 时，按 [reference.md](reference.md) 的检查项逐条看。

## 画法

- 单个 SVG，自带 `viewBox`，不引用外部图片，不写脚本
- 字体用 `Microsoft YaHei, SimHei, Noto Sans CJK SC, sans-serif`，保证转成 PNG 后中文还在
- 墨色 `#0f172a`，结果量 `#0b57d0`，被略去或很小的量 `#c2410c`，辅助线 `#94a3b8`
- 贴着线条的字加白边：`stroke="#ffffff" stroke-width="5" paint-order="stroke fill"`
- 直角用小正方形，标在真正的直角顶点上
- 尺寸被夸张时，在图内写明
- 近似不能悄悄发生：被丢掉的项用 `#c2410c` 留在等式里，并写出可用条件

几何图不要靠目测摆直角。先定坐标，使构成直角的两条方向向量点积为 0，再标符号。

完成度对照 [examples/ionosphere-right-triangle.svg](examples/ionosphere-right-triangle.svg)，不要对照聊天软件里的字符画。

## 四类画法

四类都写 SVG，立刻转成 PNG 再回复。禁止回答「画不出来」。卡住时就照对应示例改字，不要换成文字说明。符号写在图内，不靠旁边的卡片代替。

### 几何

用在距离、高度、反射、视距、直角三角形。先把两条直角边放成水平一条、竖直一条，点积为 0，再连斜边。直角标记的缺口对着斜边，并写上直角在哪个点。

图上要有：每个顶点的名字、每条边的符号、被讨论能不能略去的那一项。物理上很小的高度用橙色画长，并写「已夸大」。

电离层对照 [examples/ionosphere-right-triangle.svg](examples/ionosphere-right-triangle.svg)。视距不是这张图。两座天线的视距对照 [examples/line-of-sight.svg](examples/line-of-sight.svg)：直角在地面切点，天线在切线两端，高度沿半径方向。`d = 4.12(√ht + √hr)` 的高度单位是米、距离单位是千米，用的是等效地球半径 `4R/3`。不要把这个 4.12 代进 `R = 6371 km` 的勾股公式。

电离层图的要求：

- 直角在发射点。地心、发射点、反射点不共线
- 水平边和竖直边一个是半径 `R`，一个是切线 `x`，斜边是 `R+h`
- `h` 只标在斜边伸出地球圆弧的那一段，不标成整条斜边
- 地面弧长用灰色虚线，贴着圆弧写「弧长」，不要和蓝色切线画成同一条
- 略去 `h²` 的条件只写 `h ≪ 2R`。`h ≪ R` 只用来说明切线和弧长接近，两个条件不要写成同一个
- 给了 `R` 和 `h` 的数值时，卡片里分成三个数：切线 `√(2Rh+h²)`、略去 `h²` 后的 `√(2Rh)`、弧长 `R·atan(x/R)`

字符画把这些点排成一条直线时，那是错图。按等式画，不要把这个三角形改判成别的天波模型。

### 波形和频谱

先写横轴和纵轴的物理量、符号、单位。轴带箭头。不要画测量软件的网格，不要加公式里没有的圆点。

余弦对照 [examples/cosine-waveform.svg](examples/cosine-waveform.svg)。`v(t) = A cos(2πt/T)` 从波峰画到下一个波峰，中间只有一个波谷。`A` 是从横轴到波峰的纵轴尺寸，`T` 在横轴下方，两端对齐这两个波峰。

调幅时域单独成图，对照 [examples/am-waveform.svg](examples/am-waveform.svg)。载波是快振荡，画在包络里面。上下包络是另外两条慢变化曲线，写成式子里的 `±[...]`，不要把包络画成载波。调幅度小于 1 时，包络不穿过横轴，最窄处仍离开横轴。调幅度大于 1 时，包络穿过横轴，载波在过零处相位反相。横轴 `t`，纵轴 `s(t)`。

频谱单独成图，对照 [examples/am-spectrum.svg](examples/am-spectrum.svg)，不和时域叠在一张里。只画式子展开后真正存在的频率，谱线互不相连，每根线上写频率和高度。设 `s(t) = Ac[1 + m cos(2πf_m t)] cos(2πf_c t)`。载波高度是 `Ac`，左右边频高度都是 `Ac·m/2`，位置是 `f_c−f_m`、`f_c`、`f_c+f_m`。`Ac = 1` 时边频才是 `m/2`。没要求负频率就不画。

式子若是 `Ac cos(2πf_m t) cos(2πf_c t)`，括号里没有常数 1，这是抑制载波。对照 [examples/dsb-sc-spectrum.svg](examples/dsb-sc-spectrum.svg)：只有两条边频，高度都是 `Ac/2`，`f_c` 处不要画谱线。

抽样冲激串对照 [examples/sampling-time.svg](examples/sampling-time.svg) 和 [examples/sampling-spectrum.svg](examples/sampling-spectrum.svg)。时域相邻冲激的间隔是 `Ts`。冲激串的频谱是一串一样高的线，间隔是 `1/Ts`。这两个间隔不要画成同一个数。已抽样信号的频谱不是这三根等高线，要按原信号的形状复制。给了 `f_H` 和 `f_s` 时，对照 [examples/phone-sampling.svg](examples/phone-sampling.svg)：每份宽度是 `2f_H`，中心间隔是 `f_s`。`f_s > 2f_H` 时两份之间有空隙，写「不混叠」。`f_s = 2f_H` 时两份刚好相接，仍写「不混叠」，不要画出空隙。`f_s < 2f_H` 时两份重叠，写「混叠」。

### 框图

从左到右。一个方框只做一个运算，框里写动作，不写整句中文。箭头旁只写信号符号。公式里有几步运算，就拆成几个框，不要收成一个框。

常规调幅对照 [examples/am-block.svg](examples/am-block.svg)，不要改结构：左框「加直流 A」，右框「相乘」。箭头上依次是 `m(t)`、`A+m(t)`、`s(t)`。`c(t)` 从下方进入右框。图内写上 `c(t) = cos(2π f_c t)`。抑制载波没有常数项，对照 [examples/dsb-sc-block.svg](examples/dsb-sc-block.svg)：只留一个「相乘」框，不要画「加直流 A」。

### 电路

电阻是沿电流方向的矩形，导线在矩形两端断开。电容是两块平行板。电感是 3 到 4 个串联半圆。电压源是圆，圆内标 `+` 和 `−`。地是上长下短的三道横线。节点用实心圆点。

串联分压对照 [examples/resistor-divider.svg](examples/resistor-divider.svg)，不要改位置：左边圆圈电源，上面横着 `R1`，右边竖着 `R2`，`R2` 下面接地。`Vo` 写在 `R1` 和 `R2` 相接的节点上，并写 `Vo = Vin · R2 / (R1 + R2)`。说明里写明 `Vo` 是 `R2` 两端的电压。

`R2` 换成电容时，仍用这个骨架，电压名改到电容两端，电源和地的位置不动。不要继续写 `Vo = Vin · R2 / (R1 + R2)`。电容两端的电压另写，例如串联 RC 的稳态直流电压在电容上等于 `Vin`。

## 示例

四张完成图和电离层这道题的判断过程在 [examples.md](examples.md)。颜色、符号尺寸和检查项在 [reference.md](reference.md)。
