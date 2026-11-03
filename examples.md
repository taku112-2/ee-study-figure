# 示例

完成图：

- [ionosphere-right-triangle.svg](examples/ionosphere-right-triangle.svg)
- [cosine-waveform.svg](examples/cosine-waveform.svg)
- [am-block.svg](examples/am-block.svg)
- [resistor-divider.svg](examples/resistor-divider.svg)
- [am-waveform.svg](examples/am-waveform.svg)
- [am-spectrum.svg](examples/am-spectrum.svg)
- [sampling-time.svg](examples/sampling-time.svg)
- [sampling-spectrum.svg](examples/sampling-spectrum.svg)

这些文件由 `scripts/build_examples.py` 生成，用来对照完成度。回答学习问题时另写 `figures/` 下的新文件，不要改这些示例，也不要运行生成脚本。

## 电离层：文字示意图和等式不一致

输入是一段聊天讲解，大意是：

- 地心到发射点是 `R`
- 地心到电离层反射点是 `R+h`，并且写成斜边
- `x` 被写成发射点到反射点正下方的水平距离
- 字符画把地心、`R`、`x`、发射点排在同一条地面直线上
- 结论是 `h²` 很小，可以丢掉

先写下图必须满足的等式：

```text
(R+h)² = R² + x²
x² = 2Rh + h²
```

斜边是 `R+h`，所以直角不在地心，而在发射点。半径 `R` 和切线 `x` 互相垂直。地心、发射点、反射点分成三角形的三个顶点，不在一条直线上。字符画把 `R` 和 `x` 放在同一条直线上，和这个等式矛盾，按等式画。不要把这个直角三角形叫成错误模型，也不要用另一套天波几何代替这张图。

`x` 是切线长度。地面弧长是 `R * atan(x / R)`。只有 `h ≪ R` 时，才把切线近似叫成单程地面距离。`h²` 用橙色留在第二行，并写上条件 `h ≪ 2R`。

`R = 6371 km`、`h = 300 km` 时，`h² / 2Rh` 大约是 2.4%。图上同时给出切线、略去 `h²` 的结果、地面弧长，三个数分开写。图中的 `h` 必须注明已经夸大，否则橙段看不见。

回复说明按这个顺序写：直角在哪、三条边各是什么、近似条件、这三个长度为什么不能混成一个。

## 波形

[cosine-waveform.svg](examples/cosine-waveform.svg) 只画一个周期：`v(t) = A cos(2πt / T)`。`A` 是纵轴尺寸，`T` 是横轴尺寸，两端对齐到相邻两个波峰。

调幅时域和频谱分成两张图。包络是慢变化虚线。`[1 + m cos(2πf_m t)] cos(2πf_c t)` 的频谱是三根线：`f_c` 高度 1，两侧高度 `m/2`。

频谱沿用同一习惯：横轴频率，纵轴幅度，谱线互不相连，把式子里出现的频率都标上。

## 框图

[am-block.svg](examples/am-block.svg) 把 `s(t) = [A + m(t)] c(t)` 拆成两步：先加直流 `A`，再和 `c(t) = cos(2π f_c t)` 相乘。一个方框只做其中一步。箭头上是 `m(t)`、`A+m(t)`、`c(t)`、`s(t)`。

[dsb-sc-block.svg](examples/dsb-sc-block.svg) 是 `s(t) = m(t) c(t)`。只有「相乘」，没有加直流。

## 电路

[resistor-divider.svg](examples/resistor-divider.svg) 是串联分压：

```text
Vo = Vin · R₂ / (R₁ + R₂)
```

`Vo` 标在 `R₂` 上端节点。电阻用矩形，电源圆内标极性，地用三道缩短的横线。说明里写清 `Vo` 取的是哪一段电压。把 `R₂` 换成电容时，电源和地的位置不动，但不要再写电阻分压公式。
