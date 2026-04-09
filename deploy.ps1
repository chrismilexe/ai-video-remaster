# AI Video Remaster - Auto Deploy Script for RTX 4090
# Run: powershell -ExecutionPolicy Bypass -File deploy.ps1

$ErrorActionPreference = "Stop"

# Config
$InstallDir = "D:\AI-Tools"
$LibraryRoot = "D:\Video2AudioLibrary"
$CondaBat = "$env:USERPROFILE\miniconda3\condabin\conda.bat"

Write-Host "========================================" -ForegroundColor Magenta
Write-Host "  AI Video Remaster - Auto Deploy" -ForegroundColor Magenta
Write-Host "  Target: RTX 4090 24GB" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta

# Step 1: Check GPU
Write-Host "`n[1/6] Checking NVIDIA GPU..." -ForegroundColor Cyan
try {
    $gpu = nvidia-smi --query-gpu=name --format=csv,noheader 2>$null
    Write-Host "    Found: $gpu" -ForegroundColor Green
} catch {
    Write-Host "    ERROR: NVIDIA GPU not found!" -ForegroundColor Red
    exit 1
}

# Step 2: Check Conda
Write-Host "`n[2/6] Checking Conda..." -ForegroundColor Cyan
if (-not (Test-Path $CondaBat)) {
    Write-Host "    ERROR: Conda not found! Please run: choco install -y miniconda3" -ForegroundColor Red
    exit 1
}
Write-Host "    Conda found: $CondaBat" -ForegroundColor Green

# Step 3: Create directories
Write-Host "`n[3/6] Creating directories..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
New-Item -ItemType Directory -Force -Path $LibraryRoot, "$LibraryRoot\incoming", "$LibraryRoot\assets", "$LibraryRoot\manifests" | Out-Null
Set-Location $InstallDir

# Helper function to run conda
function Conda-Run($envName, $command) {
    & $CondaBat run -n $envName $command
}

# Step 4: Install WhisperX
Write-Host "`n[4/6] Installing WhisperX..." -ForegroundColor Cyan
Write-Host "    Creating conda environment..." -ForegroundColor Yellow
& $CondaBat create -n whisperx python=3.10 -y
Write-Host "    Installing PyTorch (CUDA 12.4)..." -ForegroundColor Yellow
& $CondaBat run -n whisperx pip install torch==2.5.1 torchvision==2.5.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124
Write-Host "    Installing WhisperX..." -ForegroundColor Yellow
& $CondaBat run -n whisperx pip install whisperx
Write-Host "    WhisperX installed!" -ForegroundColor Green

# Step 5: Install GPT-SoVITS
Write-Host "`n[5/6] Installing GPT-SoVITS..." -ForegroundColor Cyan
& $CondaBat create -n gptsovits python=3.10 -y
$gptsovitsDir = "$InstallDir\GPT-SoVITS"
if (-not (Test-Path $gptsovitsDir)) {
    Write-Host "    Downloading GPT-SoVITS..." -ForegroundColor Yellow
    git clone https://github.com/RVC-Boss/GPT-SoVITS.git
}
Set-Location $gptsovitsDir
Write-Host "    Installing dependencies..." -ForegroundColor Yellow
& $CondaBat run -n gptsovits pip install torch==2.5.1 torchvision==2.5.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124
& $CondaBat run -n gptsovits pip install -r requirements.txt

# Create start script
"@echo off`ncd /d D:\AI-Tools\GPT-SoVITS`ncall $env:USERPROFILE\miniconda3\condabin\conda.bat activate gptsovits`npython webui.py`npause" | Out-File -FilePath "$gptsovitsDir\start.bat" -Encoding ASCII
Set-Location $InstallDir
Write-Host "    GPT-SoVITS installed!" -ForegroundColor Green

# Step 6: Install MuseTalk
Write-Host "`n[6/6] Installing MuseTalk..." -ForegroundColor Cyan
& $CondaBat create -n musetalk python=3.10 -y
$musetalkDir = "$InstallDir\MuseTalk"
if (-not (Test-Path $musetalkDir)) {
    Write-Host "    Downloading MuseTalk..." -ForegroundColor Yellow
    git clone https://github.com/TMElyralab/MuseTalk.git
}
Set-Location $musetalkDir
Write-Host "    Installing PyTorch (CUDA 11.8)..." -ForegroundColor Yellow
& $CondaBat run -n musetalk pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118
Write-Host "    Installing requirements..." -ForegroundColor Yellow
& $CondaBat run -n musetalk pip install -r requirements.txt
Write-Host "    Installing MMLab components..." -ForegroundColor Yellow
& $CondaBat run -n musetalk pip install openmim
& $CondaBat run -n musetalk mim install mmengine mmcv==2.0.1 mmdet==3.1.0 mmpose==1.1.0
Set-Location $InstallDir
Write-Host "    MuseTalk installed!" -ForegroundColor Green

# Install Ollama
Write-Host "`n[Bonus] Installing Ollama..." -ForegroundColor Cyan
$ollama = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
if (-not (Test-Path $ollama)) {
    Write-Host "    Downloading Ollama..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile "$env:TEMP\ollama.exe" -UseBasicParsing
    Start-Process -FilePath "$env:TEMP\ollama.exe" -ArgumentList "/S" -Wait
    Write-Host "    Ollama installed!" -ForegroundColor Green
} else {
    Write-Host "    Ollama already installed" -ForegroundColor Green
}

# Create console script
$console = @"
@echo off
echo ========================================
echo   AI Video Remaster - Quick Console
echo ========================================
echo.
echo Environments:
echo   $env:USERPROFILE\miniconda3\condabin\conda.bat activate whisperx   (Transcription)
echo   $env:USERPROFILE\miniconda3\condabin\conda.bat activate gptsovits  (Voice Clone)
echo   $env:USERPROFILE\miniconda3\condabin\conda.bat activate musetalk   (Lip Sync)
echo.
echo Quick commands:
echo   whisperx video.mp4 --model large-v3 --language zh
echo   powershell -ExecutionPolicy Bypass -File C:\path\to\video2audio\scripts\run_batch_ingest.ps1
echo   D:\AI-Tools\GPT-SoVITS\start.bat
echo   ollama serve
echo ========================================
cmd /k
"@
$console | Out-File -FilePath "$InstallDir\console.bat" -Encoding ASCII

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nInstalled Tools:"
Write-Host "  1. WhisperX   (conda: whisperx)  - Speech to Text"
Write-Host "  2. GPT-SoVITS (conda: gptsovits) - Voice Clone"
Write-Host "  3. MuseTalk   (conda: musetalk)  - Lip Sync"
Write-Host "  4. Ollama     (system)           - Local LLM"
Write-Host "`nContent Library:"
Write-Host "  Root: $LibraryRoot"
Write-Host "  Incoming: $LibraryRoot\incoming"
Write-Host "`nNext Steps:"
Write-Host "  1. Open: $InstallDir\console.bat"
Write-Host "  2. Copy config\library.example.json -> config\library.json"
Write-Host "  3. Put videos into $LibraryRoot\incoming"
Write-Host "  4. Run scripts\run_batch_ingest.ps1 from this repo"
Write-Host "  5. Download models: ollama pull qwen2.5:32b"
Write-Host "  6. Start Web UI: python app.py"
Write-Host "========================================" -ForegroundColor Green

pause
