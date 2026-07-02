# Video to 影刀 RPA 需求文档

将操作录屏/演示视频自动整理为符合影刀（Yingdao）RPA 落地需求文档模板的 Word 文档。

## 主要功能

- 从视频文件中自动提取关键帧截图（基于场景变化检测）
- 生成标准化的影刀 RPA 需求文档（包含封面、流程基本信息、应用系统、详细步骤解析）
- 支持自定义流程步骤、系统列表、截图选择
- 模板自动填充，保留影刀 RPA logo 和装饰样式

## 目录结构

```
video-to-rpa-doc/
├── scripts/
│   ├── extract_frames.py        # 视频关键帧提取
│   ├── gen_doc.py               # 根据配置生成 Word 文档 + 流程图
│   ├── gen_flowchart.py         # 生成 Mermaid 流程图（HTML 离线可用）
│   └── create_demo_video.py     # 生成测试用模拟视频
├── references/
│   ├── 影刀RPA需求文档模板.docx  # 标准 Word 模板
│   ├── yingdao_logo.jpeg        # 封面页 Logo
│   ├── mermaid.min.js           # 流程图渲染 JS（离线使用）
│   └── template_structure.md    # 模板结构说明
├── output/                      # 示例输出目录（gitignore）
├── README.md
├── LICENSE
└── .gitignore
```

## 环境要求

- Python 3.8+
- 依赖包见 `requirements.txt`

## 运行方式

### 1. 创建虚拟环境并安装依赖

创建虚拟环境（项目根目录下）：

```bash
python -m venv env
```

激活虚拟环境：

```bash
# Windows (Git Bash)
source env/Scripts/activate

# Windows (CMD)
env\Scripts\activate.bat

# Windows (PowerShell)
env\Scripts\Activate.ps1

# macOS / Linux
source env/bin/activate
```

安装依赖：

```bash
pip install -r requirements.txt
```

### 2. 提取视频关键帧

```bash
python scripts/extract_frames.py \
    <视频文件路径> \
    <输出帧目录> \
    --threshold 30 \
    --min-interval 1.0 \
    --frame-skip 5
```

参数说明：
- `--threshold`：场景变化 MSE 阈值，越大越不敏感（默认 30）
- `--min-interval`：相邻帧最小间隔秒数（默认 1.0）
- `--frame-skip`：采样跳帧数，越大提取帧越少（默认 5）

### 3. 编写配置 config.json

根据提取的关键帧，编写流程配置 JSON 文件。参考 `output/config.json` 示例。

### 4. 生成 Word 文档

```bash
python scripts/gen_doc.py <config.json 路径>
```

## 常用命令

创建虚拟环境：

```bash
python -m venv env
```

激活虚拟环境（Git Bash）：

```bash
source env/Scripts/activate
```

安装依赖：

```bash
pip install -r requirements.txt
```

提取视频关键帧（命令行方式）：

```bash
python scripts/extract_frames.py \
    <视频文件路径> \
    <输出帧目录> \
    -t 30 -i 1.0 -s 5
```

提取视频关键帧（配置文件方式，推荐）：

```bash
python scripts/extract_frames.py extract_config.json
```

参数说明：
- `-t` / `--threshold`：场景变化 MSE 阈值，越大越不敏感（默认 30）
- `-i` / `--min-interval`：相邻帧最小间隔秒数（默认 1.0）
- `-s` / `--frame-skip`：采样跳帧数，越大提取帧越少（默认 5）

生成 Word 文档：

```bash
python scripts/gen_doc.py <config.json 路径>
```

生成示例视频：

```bash
python scripts/create_demo_video.py
```

## 生成示例视频（测试用）

如果没有现成的录屏视频，可生成模拟视频测试：

```bash
python scripts/create_demo_video.py
```

生成的视频保存到 `output/` 目录，文件名为 `demo_screen_recording_YYYYMMDD_HHMMSS.mp4`，包含 6 个场景（桌面、登录、表单、确认弹窗、成功提示、结束）。

## 作者

- **[ruixuan-xi](https://github.com/ruixuan-xi)** — 主要作者
- **zentrix566** — 辅助开发

### 致谢

特别感谢 [ruixuan-xi](https://github.com/ruixuan-xi)。

视频转影刀 RPA 需求文档的思路最初由她提出，项目的核心代码也由她提供。正是这份代码让我对这个项目有了更深入的认识。我仅在此基础上做了少量的修改和完善——没有她的原始代码和思路，就不会有这个项目。

## 许可证

[MIT](LICENSE)
