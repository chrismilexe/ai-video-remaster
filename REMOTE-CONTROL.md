# 🖥️ Mac控制4090远程机器指南

## 方案一：SSH远程执行（推荐）

### 1. 配置SSH免密登录

```bash
# 在Mac上生成密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 复制公钥到4090机器
ssh-copy-id user@192.168.1.100  # 修改为你的4090机器IP

# 测试连接
ssh user@192.168.1.100 nvidia-smi
```

### 2. 修改app.py支持远程

编辑 `app.py` 中的CONFIG:

```python
CONFIG = {
    "remote_host": "192.168.1.100",  # 你的4090机器IP
    "remote_user": "your_username",   # 你的Windows用户名
    "use_remote": True,              # 启用远程模式
    "tools_dir": "D:/AI-Tools",      # 4090机器上的工具目录
    "output_dir": "D:/AI-Outputs",   # 4090机器上的输出目录
}
```

### 3. Windows安装OpenSSH服务器

```powershell
# 在4090机器上以管理员身份运行PowerShell
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Set-Service -Name sshd -StartupType 'Automatic'
Start-Service sshd

# 防火墙放行
New-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -DisplayName "OpenSSH Server" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

---

## 方案二：共享文件夹 + 本地UI

### 1. 设置共享文件夹

**Windows端 (4090机器)**:
```powershell
# 创建共享文件夹
mkdir D:\AI-Shared
New-SmbShare -Name "AI-Shared" -Path "D:\AI-Shared" -FullAccess "Everyone"
```

**Mac端**:
```bash
# 挂载共享文件夹
mkdir -p ~/AI-Shared
mount_smbfs //guest@192.168.1.100/AI-Shared ~/AI-Shared
```

### 2. 工作流程

1. Mac上传视频到共享文件夹
2. Mac通过SSH触发4090机器处理
3. 4090机器输出结果到共享文件夹
4. Mac直接从共享文件夹获取结果

---

## 方案三：Web界面直接控制

已经内置在app.py中，启动后访问 `http://localhost:8080`

界面功能:
- 📤 上传视频文件
- ▶️ 一键启动转录
- 🎙️ 启动声音克隆WebUI
- 👄 启动对口型处理
- 📥 下载处理结果

---

## 快速命令参考

```bash
# ===== Mac上执行的常用命令 =====

# 检查4090机器状态
ssh user@192.168.1.100 nvidia-smi

# 远程启动WhisperX
ssh user@192.168.1.100 "conda activate whisperx && whisperx D:/Videos/input.mp4 --model large-v3 --language zh"

# 远程启动GPT-SoVITS (后台运行)
ssh user@192.168.1.100 "cd D:/AI-Tools/GPT-SoVITS && conda activate gptsovits && start python webui.py"

# 复制文件到4090机器
scp ~/Desktop/course.mp4 user@192.168.1.100:D:/Videos/

# 从4090机器复制结果回来
scp user@192.168.1.100:D:/AI-Outputs/*.mp4 ~/Desktop/

# 端口转发 (在Mac上访问4090的WebUI)
# 访问Mac的 localhost:19874 会转发到4090的 9874
ssh -L 19874:localhost:9874 user@192.168.1.100

# 同时转发多个端口
ssh -L 19874:localhost:9874 -L 18000:localhost:8000 -L 17860:localhost:7860 user@192.168.1.100
```

---

## 端口转发配置表

| 服务 | 4090端口 | Mac转发端口 | 访问地址 |
|------|----------|-------------|----------|
| GPT-SoVITS | 9874 | 19874 | http://localhost:19874 |
| CosyVoice | 8000 | 18000 | http://localhost:18000 |
| FishSpeech | 7860 | 17860 | http://localhost:17860 |
| Ollama | 11434 | 11434 | http://localhost:11434 |
| MuseTalk API | 待定 | - | - |

---

## 一键转发脚本

创建 `~/forward-ports.sh`:

```bash
#!/bin/bash
REMOTE="user@192.168.1.100"

echo "🔌 建立端口转发..."
echo "GPT-SoVITS: http://localhost:19874"
echo "CosyVoice:  http://localhost:18000"
echo "FishSpeech: http://localhost:17860"
echo "Ollama:     http://localhost:11434"
echo "按 Ctrl+C 停止转发"

ssh -N \
    -L 19874:localhost:9874 \
    -L 18000:localhost:8000 \
    -L 17860:localhost:7860 \
    -L 11434:localhost:11434 \
    $REMOTE
```

使用:
```bash
chmod +x ~/forward-ports.sh
~/forward-ports.sh
```

---

## 自动化部署脚本 (4090机器)

创建 `D:/deploy-ai-tools.ps1`:

```powershell
# AI工具自动部署脚本 (Windows 4090机器)
$ErrorActionPreference = "Stop"

# 配置
$InstallDir = "D:\AI-Tools"
$CondaPath = "$env:USERPROFILE\miniconda3\Scripts\conda.exe"

# 创建目录
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
Set-Location $InstallDir

# 安装Miniconda (如果未安装)
if (-not (Test-Path $CondaPath)) {
    Write-Host "📦 安装Miniconda..."
    $url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
    $output = "$env:TEMP\miniconda.exe"
    Invoke-WebRequest -Uri $url -OutFile $output
    Start-Process -FilePath $output -ArgumentList "/S", "/D=$env:USERPROFILE\miniconda3" -Wait
}

# 安装Git (如果未安装)
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "📦 安装Git..."
    winget install -e --id Git.Git
}

# 安装FFmpeg (如果未安装)
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Host "📦 安装FFmpeg..."
    winget install -e --id Gyan.FFmpeg
}

# 安装CUDA工具 (如果未安装)
$nvidiaSmi = Get-Command nvidia-smi -ErrorAction SilentlyContinue
if (-not $nvidiaSmi) {
    Write-Host "⚠️  请手动安装NVIDIA驱动和CUDA 12.4"
    Write-Host "    https://developer.nvidia.com/cuda-downloads"
}

# 创建所有conda环境
$Environments = @(
    @{Name="whisperx"; Packages=@("torch==2.5.1", "torchvision", "torchaudio", "whisperx")},
    @{Name="gptsovits"; Git="https://github.com/RVC-Boss/GPT-SoVITS.git"; Script="install.ps1"},
    @{Name="cosyvoice"; Git="https://github.com/FunAudioLLM/CosyVoice.git"},
    @{Name="fishspeech"; Git="https://github.com/fishaudio/fish-speech.git"},
    @{Name="musetalk"; Git="https://github.com/TMElyralab/MuseTalk.git"}
)

foreach ($env in $Environments) {
    Write-Host "🚀 设置环境: $($env.Name)"
    
    # 创建环境
    & $CondaPath create -n $env.Name python=3.10 -y
    
    # 克隆仓库
    if ($env.Git) {
        $repoName = [System.IO.Path]::GetFileNameWithoutExtension($env.Git)
        if (-not (Test-Path $repoName)) {
            git clone $env.Git
        }
    }
    
    # 安装依赖
    if ($env.Packages) {
        $packages = $env.Packages -join " "
        & $CondaPath run -n $env.Name pip install $packages
    }
}

Write-Host "✅ 部署完成!"
Write-Host "请手动下载预训练模型到对应目录"
```

---

## 故障排除

### SSH连接失败
```bash
# 检查4090机器IP
ipconfig  # Windows

# 测试连通性
ping 192.168.1.100

# 检查SSH服务
ssh user@192.168.1.100 -v
```

### 显存不足
```bash
# 远程检查显存
ssh user@192.168.1.100 "nvidia-smi --query-gpu=memory.used,memory.free --format=csv"

# 清理显存
ssh user@192.168.1.100 "nvidia-smi --gpu-reset -i 0"
```

### 网络慢
```bash
# 使用rsync替代scp (需要安装cwRsync或WSL)
rsync -avz --progress user@192.168.1.100:/remote/path /local/path
```

---

**今晚部署步骤**:
1. 在4090机器上运行 `deploy-ai-tools.ps1`
2. 在Mac上配置SSH免密登录
3. 在Mac上运行 `python app.py`
4. 浏览器访问 `http://localhost:8080` 开始控制
