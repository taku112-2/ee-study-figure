# ee-study-figure

电子信息课程用的作图技能。豆包、ChatGPT、Cursor 都能用。把一段讲解画成示意图，让图上的标注和公式是同一套关系。

聊天机器人讲反射、波形、框图和电路时，有时不画图，改用字符拼一张示意图。字符对不齐时，直角和斜边会看错。装上这个技能后，它会按课程里的关系把图画出来。

## 示例

电离层反射。原讲解把地球半径 `R` 和距离 `x` 排在同一条直线上，同时把 `R+h` 写成斜边。按这个等式，直角在发射点：`R` 沿半径，`x` 沿切线。`h` 在图上被夸大，否则几乎看不见。

![电离层直角三角形](examples/ionosphere-right-triangle.svg)

另外三类的完成度：

![余弦信号](examples/cosine-waveform.svg)

![幅度调制](examples/am-block.svg)

![串联分压](examples/resistor-divider.svg)

## 能画的四类

- 几何模型：反射、视距、直角三角形
- 波形和频谱
- 系统框图
- 基础电路，例如分压。不画 PCB，也不画器件照片

## 安装

三个地方用的是同一个文件夹，`SKILL.md` 就在这一层。不要改里面的文件。

豆包：打开技能页面，选择上传文件夹，选中本文件夹。

ChatGPT：打开 Skills，选择 Create，再选择 Upload from your computer，选中本文件夹。装好后在对话里输入 `@`，选 `ee-study-figure`。

Cursor：把本文件夹复制到个人技能目录。

Windows：

```bat
xcopy /E /I . %USERPROFILE%\.cursor\skills\ee-study-figure
```

macOS / Linux：

```bash
mkdir -p ~/.cursor/skills
cp -R . ~/.cursor/skills/ee-study-figure
```

## 使用

把讲解贴进已经装好技能的对话，然后说：

```text
画成示意图
```

第一次回复里应是一张 PNG。图下面会说明每个符号、等式，以及近似在什么条件下成立。

## 检查示例

只使用 Python 标准库：

```bash
python scripts/build_examples.py
python scripts/check_examples.py
```

## 目录

- `SKILL.md`：技能说明
- `examples/`：示例图
- `scripts/check_svg.py`：检查图是否自包含、是否带上指定标注
