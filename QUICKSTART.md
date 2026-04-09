# 🚀 今晚部署快速指南

> ⚡ **目标**: 3小时内在4090机器上完成全套AI视频重制系统部署  
> 📅 **日期**: 2026年3月23日  
> 💻 **硬件**: RTX 4090 24GB

---

## 📋 部署前检查清单

### 4090机器端 (Windows 11)
- [ ] NVIDIA驱动 >= 546.33
- [ ] CUDA 12.4 已安装
- [ ] 100GB+ 磁盘空间 (SSD)
- [ ] 网络连接正常

### Mac端
- [ ] Python 3.10+ 已安装
- [ ] 与4090机器在同一局域网

---

## ⏱️ 时间线 (预估3小时)

### 阶段1: 环境准备 (30分钟)

**在4090机器上执行**:

```powershell
# 以管理员身份打开 PowerShell

# 1. 安装Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 2. 安装基础工具
choco install -y git ffmpeg cuda miniconda3

# 3. 重启PowerShell，验证安装
nvidia-smi  # 应该显示RTX 4090信息
conda --version  # 应该显示版本号
```

---

### 阶段2: 核心工具安装 (90分钟)

按顺序安装，每个约20-30分钟（含模型下载）:

#### 1. WhisperX (必须) - 20分钟

```powershell
# 创建环境
conda create -n whisperx python=3.10 -y
conda activate whisperx

# 安装PyTorch (CUDA 12.4)
pip install torch==2.5.1 torchvision==2.5.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124

# 安装WhisperX
pip install whisperx

# 测试 (首次运行会下载模型)
whisperx --help
```

#### 2. GPT-SoVITS (必须) - 30分钟

**推荐：使用一键整合包** (更快)

```powershell
# 方法A: 一键包 (推荐)
# 1. 浏览器下载: https://github.com/RVC-Boss/GPT-SoVITS/releases
# 2. 解压到 D:\AI-Tools\GPT-SoVITS
# 3. 双击 go-webui.bat 启动

# 方法B: 手动安装
cd D:\
mkdir AI-Tools
cd AI-Tools
conda create -n gptsovits python=3.10 -y
conda activate gptsovits
git clone https://github.com/RVC-Boss/GPT-SoVITS.git
cd GPT-SoVITS
powershell -ExecutionPolicy ByPass -File install.ps1 --Device CU124 --Source HF
```

**模型下载** (约5GB，自动下载):
- s2G488k.pth
- s2D488k.pth  
- s1bert25hz-5kh-longer-epoch=12-step=369668.ckpt

#### 3. MuseTalk (必须) - 30分钟

```powershell
cd D:\AI-Tools
conda create -n musetalk python=3.10 -y
conda activate musetalk

git clone https://github.com/TMElyralab/MuseTalk.git
cd MuseTalk

# 安装PyTorch
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118

# 安装依赖
pip install -r requirements.txt

# 安装MMLab
pip install --no-cache-dir -U openmim
mim install mmengine
mim install "mmcv==2.0.1"
mim install "mmdet==3.1.0"
mim install "mmpose==1.1.0"

# 下载模型 (按README指引)
```

#### 4. Ollama + Qwen2.5 (推荐) - 20分钟

```powershell
# 下载安装: https://ollama.com/download
# 安装完成后，在PowerShell执行:

ollama pull qwen2.5:32b

# 测试
ollama run qwen2.5:32b "你好"
```

---

### 阶段3: Mac端UI启动 (10分钟)

**在Mac上执行**:

```bash
cd /Users/chris/Project/video2audio

# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置远程连接
# 编辑 app.py 修改 CONFIG:
#   "remote_host": "你的4090机器IP",
#   "use_remote": True,

# 3. 启动UI
python app.py

# 4. 浏览器访问 http://localhost:8080
```

---

### 阶段4: 端到端测试 (30分钟)

使用一个短视频测试完整流程:

1. **转录测试** (5分钟)
   - UI中上传测试视频
   - 点击"开始转录"
   - 检查输出的 `.srt` 文件

2. **声音克隆测试** (15分钟)
   - 在4090机器上访问 http://localhost:9874 (GPT-SoVITS)
   - 上传5秒你的声音样本
   - 点击训练 (约5分钟)
   - 输入文字生成测试音频

3. **对口型测试** (10分钟)
   - UI中配置原视频 + 新音频
   - 选择 MuseTalk
   - 点击"开始对口型"

---

## 🎯 验证清单

部署完成后，确认以下功能正常:

- [ ] WhisperX可以识别视频并生成字幕
- [ ] GPT-SoVITS可以克隆声音并生成音频
- [ ] MuseTalk可以合成对口型视频
- [ ] Mac可以通过UI控制4090机器
- [ ] Ollama可以回答文稿优化问题

---

## 🐛 常见问题速查

### 显存不足 (OOM)
```powershell
# 检查显存占用
nvidia-smi

# 解决方案:
# 1. 关闭其他程序
# 2. 使用更小模型 (large-v3 → medium)
# 3. 降低批处理大小
```

### 模型下载慢
```powershell
# 设置镜像
$env:HF_ENDPOINT = "https://hf-mirror.com"

# 或在conda环境变量中设置
conda env config vars set HF_ENDPOINT=https://hf-mirror.com -n whisperx
```

### Python包冲突
```powershell
# 删除环境重建
conda remove -n whisperx --all
conda create -n whisperx python=3.10 -y
```

### 端口被占用
```powershell
# 查看端口占用
netstat -ano | findstr :9874

# 结束进程
taskkill /F /PID <进程ID>
```

---

## 📁 部署完成后的目录结构

```
D:\AI-Tools\
├── GPT-SoVITS\          # 约10GB (含模型)
├── MuseTalk\             # 约5GB (含模型)
├── WhisperX\             # 约5GB (conda环境)
├── Ollama\               # 约20GB (模型)
└── Outputs\              # 输出目录
    ├── transcripts\      # 字幕文件
    ├── audio\            # 生成音频
    └── videos\           # 最终视频

D:\Video2AudioLibrary\
├── incoming\             # 待批量转录视频
├── assets\               # 单条资产目录
└── manifests\            # 内容库索引
```

---

## 🎉 部署成功标志

当你可以在Mac上打开 http://localhost:8080 并:
1. 看到所有工具状态为"已安装"
2. 点击"启动"能打开各工具的WebUI
3. 上传视频后能生成字幕
4. 声音克隆后生成的新音频听起来像你的声音

**恭喜你！部署成功！**

---

## 📞 下一步

1. **复制配置**:
   `Copy-Item .\config\library.example.json .\config\library.json`
2. **放入素材**:
   把视频放进 `D:\Video2AudioLibrary\incoming`
3. **批量入库**:
   `powershell -ExecutionPolicy Bypass -File .\scripts\run_batch_ingest.ps1`
4. **优化工作流**: 参考 MODELS-2026.md 调整参数
5. **自动化**: 配置 n8n/Activepieces 自动工作流

**预计处理速度**:
- 1小时课程视频 → 约10分钟完成全套流程
- 批量10个视频 → 约1.5小时

---

**祝部署顺利！有问题随时问 Kimi Code 🚀**
