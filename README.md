# 🎬 AI视频重制系统 - 项目总览

> 在 RTX 4090 上本地部署全流程AI视频重制工具链  
> 从Mac通过Web UI远程控制

## 当前内容品牌

- Show Name: `The Outcome Code`
- Tagline: `A Practical System for Reading People, Pressure, and Timing`
- 当前内容方向：用中国传统模式分析去解释人、压力、时机与结果
- 当前标题公式：`一个现实问题 + 一个模式判断 + 一个结果承诺`

---

## 📦 项目结构

```
video2audio/
├── 📄 README.md              # 本文件 - 项目总览
├── 📄 README-DEPLOY.md       # 详细部署文档
├── 📄 QUICKSTART.md          # 快速启动指南 (今晚用)
├── 📄 MODELS-2026.md         # 2026年3月最新模型推荐
├── 📄 REMOTE-CONTROL.md      # Mac远程控制4090指南
├── 📄 requirements.txt       # Python依赖
├── 📁 config/                # 本地内容库配置样例
│   └── library.example.json
│
├── 🐍 app.py                 # 主Web UI应用 (Mac上运行)
├── 🖥️ start.sh               # Mac启动脚本
├── 🖥️ start.bat              # Windows启动脚本 (备用)
├── 📁 scripts/               # 批量入库与脚本资产
│   ├── batch_ingest.py
│   └── run_batch_ingest.ps1
│
├── 📁 templates/             # Web界面模板
│   └── index.html            # 主控制面板
│
└── 📁 static/                # 静态资源
```

---

## 🚀 快速开始 (今晚执行)

### 步骤1: 4090机器部署 (2-3小时)

```powershell
# 1. 在4090机器上以管理员打开PowerShell
# 2. 按顺序执行:

# 安装Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 安装基础环境
choco install -y git ffmpeg cuda miniconda3

# 详细步骤参考 QUICKSTART.md
```

### 步骤2: Mac端启动UI

```bash
cd /Users/chris/Project/video2audio
pip install -r requirements.txt
python app.py

# 浏览器访问 http://localhost:8080
```

### 步骤3: 4090机器批量入库文稿

```powershell
# 在仓库根目录执行
Copy-Item .\config\library.example.json .\config\library.json

# 把视频放到 D:\Video2AudioLibrary\incoming

# 执行批量入库
powershell -ExecutionPolicy Bypass -File .\scripts\run_batch_ingest.ps1

# 可选快速试跑
powershell -ExecutionPolicy Bypass -File .\scripts\run_batch_ingest.ps1 --fast --limit 5
```

---

## 📚 文档导航

| 文档 | 用途 | 什么时候看 |
|------|------|-----------|
| **QUICKSTART.md** | 今晚部署步骤 | 🎯 **现在就看** |
| **README-DEPLOY.md** | 详细部署说明 | 遇到问题查看 |
| **MODELS-2026.md** | 模型选择与优化 | 部署完成后调优 |
| **REMOTE-CONTROL.md** | 远程控制配置 | 需要SSH控制时 |
| **docs/WINDOWS11_BATCH_INGEST_RUNBOOK.md** | Windows 11 批量入库执行手册 | 回家后直接按它跑 |

---

## 🎯 核心功能

### 1. 语音转文字 (WhisperX)
- **显存**: 10GB
- **速度**: 70倍实时 (1小时视频约1分钟)
- **质量**: 95%准确率 (large-v3)
- **功能**: 自动说话人分离

### 2. 声音克隆 (GPT-SoVITS)
- **显存**: 8-12GB
- **样本**: 仅需1分钟你的声音
- **质量**: 中文效果业界最佳
- **功能**: 跨语言、情感控制

### 3. 对口型 (MuseTalk + VideoReTalking)
- **显存**: 6-8GB
- **速度**: 
  - MuseTalk: 实时 30fps (快速预览)
  - VideoReTalking: 2s/帧 (最终成品)
- **质量**: 广播级

### 4. 本地LLM (Ollama + Qwen2.5-32B)
- **显存**: 20GB
- **用途**: 文稿优化、翻译、摘要
- **速度**: 20 tokens/s

---

## 💻 系统要求

### 4090机器 (Windows 11/Linux)
- **显卡**: NVIDIA RTX 4090 24GB
- **CPU**: i9/R9 或同级别
- **内存**: 32GB+ (推荐64GB)
- **磁盘**: 100GB+ SSD
- **网络**: 局域网可达

### Mac控制端
- **系统**: macOS 12+
- **Python**: 3.10+
- **内存**: 8GB+

---

## 🌐 Web UI界面

启动后访问 http://localhost:8080

### 功能模块

1. **⚡ 快速工作流**
   - 一键转录视频
   - 一键对口型
   - 批量处理

2. **🛠️ 工具管理**
   - 查看各工具状态
   - 一键安装/启动/停止
   - 实时日志查看

3. **📁 输出文件**
   - 字幕文件 (.srt)
   - 音频文件 (.wav)
   - 视频文件 (.mp4)

---

## 🗂️ 批量内容库

长期内容库默认放在仓库外：

`D:\Video2AudioLibrary`

目录结构：

```text
D:\Video2AudioLibrary\
├── incoming\                 # 待处理视频
├── assets\
│   └── <asset_id>\
│       ├── transcript.srt
│       ├── transcript.json
│       ├── raw_zh.md
│       └── metadata.json
└── manifests\
    └── library_index.jsonl
```

第一版的目标是先把本地视频稳定转成中文文稿资产，作为后续主题总稿、英文主稿和时事结合创作的基础库。

---

## 🔧 工具链组件

| 工具 | 版本 | 用途 | 端口 |
|------|------|------|------|
| WhisperX | latest | 语音转文字 | - |
| GPT-SoVITS | v2 | 声音克隆 | 9874 |
| CosyVoice | 300M | 阿里TTS | 8000 |
| FishSpeech | v1.5 | 多语言TTS | 7860 |
| MuseTalk | latest | 实时对口型 | - |
| VideoReTalking | latest | 高质量对口型 | - |
| Ollama | latest | 本地LLM | 11434 |

---

## 📊 性能预期 (4090)

| 任务 | 10分钟视频 | 1小时视频 |
|------|-----------|-----------|
| 转录 | ~8秒 | ~50秒 |
| 声音克隆 | ~30秒 | ~3分钟 |
| 对口型(MuseTalk) | ~10秒 | ~1分钟 |
| 对口型(VideoReTalking) | ~5分钟 | ~30分钟 |
| **总计** | **~6分钟** | **~35分钟** |

---

## ⚠️ 重要提示

### 模型下载
首次部署需要下载约 **50GB** 模型文件:
- Whisper large-v3: ~3GB
- GPT-SoVITS: ~5GB
- CosyVoice: ~3GB
- MuseTalk: ~5GB
- Qwen2.5-32B: ~20GB

**建议**: 使用国内镜像加速下载

### 显存管理
- 4090的24GB显存**足够**同时运行转录+声音克隆
- 对口型需要独占显卡，建议分开执行

### 网络要求
- Mac和4090机器需要在同一局域网
- 或通过VPN/公网IP连接

---

## 🐛 故障排除

### 显存不足
```python
# 使用更小模型
whisperx video.mp4 --model medium  # 替代 large-v3
```

### 模型下载失败
```bash
# 设置镜像
export HF_ENDPOINT=https://hf-mirror.com
```

### 端口冲突
```bash
# 查看端口占用
lsof -i :9874
```

---

## 📝 更新日志

### 2026-03-23
- ✅ 更新至最新模型版本
- ✅ 添加MuseTalk实时对口型
- ✅ 添加GPT-SoVITS v2支持
- ✅ 优化4090显存配置

---

## 📞 获取帮助

1. 查看各文档的"常见问题"章节
2. 检查各工具的GitHub Issues
3. 使用Kimi Code继续提问

---

## 🏆 最终目标

部署完成后，你可以在Mac上:
1. 上传课程视频
2. 一键生成字幕
3. 用你的声音生成新音频
4. 合成对口型视频

**全程无需命令行，全部通过Web界面点击完成！**

---

**开始部署**: 打开 **QUICKSTART.md** 按照步骤执行 🚀
