# 🎬 本地AI视频重制系统部署指南

> **最后更新**: 2026年3月23日  
> **适用硬件**: RTX 4090 (24GB VRAM) + 64GB RAM + i9/R9 顶配CPU  
> **操作系统**: Windows 11 / Ubuntu 22.04 / WSL2

---

## 📋 部署前准备

### 硬件确认清单
- [ ] NVIDIA RTX 4090 显卡已安装
- [ ] 驱动版本 >= 535.54.03 (Linux) / >= 546.33 (Windows)
- [ ] CUDA 12.4+ 已安装
- [ ] 至少 100GB 可用磁盘空间 (SSD)
- [ ] 850W+ 电源已连接

### 快速检查命令
```bash
# 检查显卡
nvidia-smi

# 预期输出显示:
# NVIDIA GeForce RTX 4090, 24576 MiB, CUDA Version: 12.4+
# 显存占用应低于 2GB (未运行模型时)
```

---

## 🚀 一键部署脚本

### 步骤1: 安装基础环境 (复制到PowerShell/终端执行)

```powershell
# ===== Windows 用户执行此部分 =====
# 以管理员身份打开 PowerShell

# 1. 安装 Chocolatey (包管理器)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 2. 安装必要工具
choco install -y git ffmpeg cuda miniconda3

# 3. 重启 PowerShell，然后验证
ffmpeg -version
conda --version
nvidia-smi
```

```bash
# ===== Linux/WSL2 用户执行此部分 =====
# 1. 安装基础依赖
sudo apt update && sudo apt install -y git ffmpeg wget curl

# 2. 安装 Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
source $HOME/miniconda3/etc/profile.d/conda.sh
conda init bash
source ~/.bashrc

# 3. 验证
conda --version
ffmpeg -version
nvidia-smi
```

---

## 🎯 核心组件部署

### 1️⃣ WhisperX (语音转文字)

**显存占用**: ~10GB  
**处理速度**: 70倍实时 (4090上1小时视频约1分钟处理完)

```bash
# 创建环境
conda create -n whisperx python=3.10 -y
conda activate whisperx

# 安装 PyTorch (CUDA 12.4)
pip install torch==2.5.1 torchvision==2.5.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124

# 安装 WhisperX
pip install whisperx

# 下载模型 (首次运行会自动下载，也可手动预下载)
whisperx --model large-v3 --help

# 测试运行
whisperx sample_video.mp4 --model large-v3 --language zh --diarize --output_format srt
```

**模型选择指南**:
| 模型 | 显存需求 | 速度 | 准确率 | 适用场景 |
|------|----------|------|--------|----------|
| tiny | ~1GB | 1000x | 75% | 快速测试 |
| base | ~1GB | 500x | 80% | 实时应用 |
| small | ~2GB | 250x | 85% | 平衡选择 |
| medium | ~5GB | 100x | 90% | 日常使用 |
| large-v3 | ~10GB | 70x | 95% | **推荐** |
| large-v3-turbo | ~6GB | 150x | 92% | 快速+质量平衡 |

---

### 2️⃣ GPT-SoVITS (声音克隆 - 中文首选)

**显存占用**: 8-12GB (推理) / 16GB (训练)  
**声音质量**: ⭐⭐⭐⭐⭐ 中文效果最佳

```bash
# 方法A: 一键整合包 (推荐新手)
# 下载地址: https://github.com/RVC-Boss/GPT-SoVITS/releases
# 下载后解压，双击 go-webui.bat 即可

# 方法B: 手动安装 (推荐开发者)
conda create -n gptsovits python=3.10 -y
conda activate gptsovits

# 克隆仓库
cd D:\AI-Tools  # 修改为你的安装目录
git clone https://github.com/RVC-Boss/GPT-SoVITS.git
cd GPT-SoVITS

# Windows 安装脚本
powershell -ExecutionPolicy ByPass -File install.ps1 --Device CU124 --Source HF

# 或手动安装依赖
pip install -r requirements.txt

# 下载预训练模型
# 模型会自动下载到 GPT_SoVITS/pretrained_models/

# 启动
python webui.py
```

**访问**: http://localhost:9874  
**使用步骤**:
1. 上传5-30秒的声音样本
2. 点击"开始训练" (1-5分钟)
3. 输入文字生成语音

---

### 3️⃣ CosyVoice (阿里出品 - 中文TTS)

**显存占用**: 6-10GB  
**特点**: 支持流式输出，150ms延迟

```bash
conda create -n cosyvoice python=3.10 -y
conda activate cosyvoice

# 克隆仓库
cd D:\AI-Tools
git clone https://github.com/FunAudioLLM/CosyVoice.git
cd CosyVoice

# 安装依赖
pip install -r requirements.txt
pip install -e .

# 下载模型
# 方法1: 自动下载 (首次运行)
# 方法2: 手动下载 ModelScope
pip install modelscope
python -c "from modelscope import snapshot_download; snapshot_download('iic/CosyVoice-300M', local_dir='pretrained_models/CosyVoice-300M')"

# 启动WebUI
python webui.py

# 或启动API服务
python api.py
```

**访问**: http://localhost:8000

---

### 4️⃣ Fish Speech (最新开源TTS)

**显存占用**: 6-8GB  
**特点**: 支持多语言代码切换，Apache 2.0可商用

```bash
conda create -n fishspeech python=3.10 -y
conda activate fishspeech

cd D:\AI-Tools
git clone https://github.com/fishaudio/fish-speech.git
cd fish-speech

# 安装
pip install -e .

# 下载模型 (V1.5)
python -m fish_speech.download_models --model fish-speech-1.5

# 启动WebUI
python -m fish_speech.webui
```

**访问**: http://localhost:7860

---

### 5️⃣ MuseTalk (实时对口型)

**显存占用**: 6-8GB  
**处理速度**: 实时 ~30fps (4090)

```bash
conda create -n musetalk python=3.10 -y
conda activate musetalk

cd D:\AI-Tools
git clone https://github.com/TMElyralab/MuseTalk.git
cd MuseTalk

# 安装 PyTorch
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118

# 安装依赖
pip install -r requirements.txt

# 安装 MMLab 系列
pip install --no-cache-dir -U openmim
mim install mmengine
mim install "mmcv==2.0.1"
mim install "mmdet==3.1.0"
mim install "mmpose==1.1.0"

# 下载模型 (按官方README指引)
# 模型文件会下载到 models/ 目录

# 运行推理
python inference.py --video_path input.mp4 --audio_path audio.wav --output_path output.mp4
```

---

### 6️⃣ VideoReTalking (高质量对口型)

**显存占用**: 6-8GB  
**特点**: 后处理导向，质量最高但较慢

```bash
conda create -n retalking python=3.8 -y
conda activate retalking

cd D:\AI-Tools
git clone https://github.com/OpenTalker/video-retalking.git
cd video-retalking

# 安装依赖
pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
pip install -r requirements.txt

# 下载预训练模型
# 按 README 中的 Google Drive 或 Baidu 网盘链接下载
# 解压到 checkpoints/ 目录

# 运行
python inference.py --face input.mp4 --audio audio.wav --outfile output.mp4
```

---

## 🧠 本地LLM部署 (文稿优化/翻译)

### Ollama (最简单)

```bash
# Windows: 下载安装包 https://ollama.com/download
# Linux:
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型
ollama pull qwen2.5:32b    # 通义千问 32B，中文优化
ollama pull llama3.3:70b   # Llama 3.3 70B
ollama pull deepseek-v3    # DeepSeek V3

# 运行
ollama run qwen2.5:32b

# API调用
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:32b",
  "prompt": "优化这段课程文稿，去除口头禅..."
}'
```

### LM Studio (图形界面)

```bash
# 下载: https://lmstudio.ai/
# 安装后界面操作:
# 1. 搜索模型 (如 qwen2.5-32b)
# 2. 下载模型
# 3. 启动本地服务器 (默认端口 1234)
```

---

## 📁 目录结构建议

```
D:\AI-Tools\
├── GPT-SoVITS\          # 声音克隆 (中文首选)
├── CosyVoice\            # 阿里TTS
├── Fish-Speech\          # Fish TTS
├── WhisperX\             # 语音转文字
├── MuseTalk\             # 实时对口型
├── VideoReTalking\       # 高质量对口型
├── Ollama\               # 本地LLM
├── Models\               # 共享模型目录
│   ├── whisper\
│   ├── gpt-sovits\
│   ├── cosyvoice\
│   └── musetalk\
└── Outputs\              # 输出目录
    ├── transcripts\
    ├── audio\
    └── videos\
```

---

## ⚡ 性能优化 (4090专属)

### 1. 启用 TensorRT 加速

```bash
# 部分模型支持 TensorRT 加速
# 以 Whisper 为例
pip install faster-whisper
# 使用 --compute_type float16 或 int8
whisperx video.mp4 --compute_type float16
```

### 2. 多显卡优化 (如果有第二张卡)

```python
# 设置可见GPU
export CUDA_VISIBLE_DEVICES=0  # 只用第一张4090
```

### 3. 显存管理

```bash
# 监控显存
nvidia-smi -l 1

# 清理显存 (模型崩溃后)
nvidia-smi --gpu-reset -i 0
```

---

## 🐛 常见问题

### Q: CUDA out of memory
```bash
# 解决方案1: 使用更小模型
whisperx video.mp4 --model medium  # 替代 large-v3

# 解决方案2: 降低精度
whisperx video.mp4 --compute_type int8

# 解决方案3: 分块处理
whisperx video.mp4 --chunk_size 20  # 默认30，改小
```

### Q: 模型下载速度慢
```bash
# 使用镜像
export HF_ENDPOINT=https://hf-mirror.com
# 或在 Windows:
set HF_ENDPOINT=https://hf-mirror.com
```

### Q: Windows 路径问题
```python
# 使用双反斜杠或原始字符串
path = "D:\\AI-Tools\\GPT-SoVITS"
# 或
path = r"D:\AI-Tools\GPT-SoVITS"
```

---

## 🎯 今晚部署优先级

按此顺序部署，每完成一个就测试：

1. **WhisperX** (必须) - 转录是第一步
2. **GPT-SoVITS** (必须) - 中文声音克隆核心
3. **MuseTalk** (必须) - 对口型
4. **Ollama + Qwen2.5** (推荐) - 文稿优化
5. **CosyVoice/FishSpeech** (可选) - 备选TTS

**预计总时间**: 2-3小时 (含下载模型)

---

## 📞 回到 Mac 后的操作

在 Mac 上运行项目中的 UI 界面，它会通过局域网/SSH 控制 Windows 4090 机器：

```bash
# 在 Mac 上 (当前目录)
cd /Users/chris/Project/video2audio
python app.py

# 然后浏览器打开 http://localhost:8080
```

UI 界面会自动通过 SSH 在 4090 机器上执行命令。
