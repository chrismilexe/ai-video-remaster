# Fix Installation Script
$ErrorActionPreference = "Stop"

$CondaBat = "$env:USERPROFILE\miniconda3\condabin\conda.bat"
$InstallDir = "D:\AI-Tools"
$LibraryRoot = "D:\Video2AudioLibrary"

Write-Host "========================================" -ForegroundColor Green
Write-Host "  Fixing AI Tools Installation" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
New-Item -ItemType Directory -Force -Path $LibraryRoot, "$LibraryRoot\incoming", "$LibraryRoot\assets", "$LibraryRoot\manifests" | Out-Null

# 1. WhisperX
Write-Host "`n[1/3] Setting up WhisperX..." -ForegroundColor Cyan
& $CondaBat create -n whisperx python=3.10 -y
Write-Host "Installing PyTorch..." -ForegroundColor Yellow
& $CondaBat run -n whisperx pip install torch==2.5.1 torchvision==2.5.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124 --quiet
Write-Host "Installing WhisperX..." -ForegroundColor Yellow
& $CondaBat run -n whisperx pip install whisperx --quiet
Write-Host "WhisperX OK!" -ForegroundColor Green

# 2. GPT-SoVITS
Write-Host "`n[2/3] Setting up GPT-SoVITS..." -ForegroundColor Cyan
& $CondaBat create -n gptsovits python=3.10 -y
Set-Location "$InstallDir\GPT-SoVITS"
Write-Host "Installing dependencies..." -ForegroundColor Yellow
& $CondaBat run -n gptsovits pip install torch==2.5.1 torchvision==2.5.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124 --quiet
& $CondaBat run -n gptsovits pip install -r requirements.txt --quiet
Write-Host "GPT-SoVITS OK!" -ForegroundColor Green

# 3. MuseTalk
Write-Host "`n[3/3] Setting up MuseTalk..." -ForegroundColor Cyan
& $CondaBat create -n musetalk python=3.10 -y
Set-Location "$InstallDir\MuseTalk"
Write-Host "Installing PyTorch..." -ForegroundColor Yellow
& $CondaBat run -n musetalk pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118 --quiet
Write-Host "Installing requirements..." -ForegroundColor Yellow
& $CondaBat run -n musetalk pip install -r requirements.txt --quiet
Write-Host "Installing MMLab..." -ForegroundColor Yellow
& $CondaBat run -n musetalk pip install openmim --quiet
& $CondaBat run -n musetalk mim install mmengine mmcv==2.0.1 mmdet==3.1.0 mmpose==1.1.0 --quiet
Write-Host "MuseTalk OK!" -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  All environments fixed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Content library root: $LibraryRoot" -ForegroundColor Green
