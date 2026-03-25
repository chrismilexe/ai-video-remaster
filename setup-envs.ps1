# Setup Conda Environments
$ErrorActionPreference = "Stop"
$CondaBat = "$env:USERPROFILE\miniconda3\condabin\conda.bat"
$InstallDir = "D:\AI-Tools"

Write-Host "Creating conda environments..." -ForegroundColor Green

# WhisperX
Write-Host "`n[1/3] Creating whisperx environment..." -ForegroundColor Cyan
& $CondaBat create -n whisperx python=3.10 -y
& $CondaBat run -n whisperx pip install torch==2.5.1 torchvision==2.5.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124
& $CondaBat run -n whisperx pip install whisperx
Write-Host "whisperx DONE" -ForegroundColor Green

# GPT-SoVITS
Write-Host "`n[2/3] Creating gptsovits environment..." -ForegroundColor Cyan
& $CondaBat create -n gptsovits python=3.10 -y
Set-Location "$InstallDir\GPT-SoVITS"
& $CondaBat run -n gptsovits pip install torch==2.5.1 torchvision==2.5.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124
& $CondaBat run -n gptsovits pip install -r requirements.txt
Write-Host "gptsovits DONE" -ForegroundColor Green

# MuseTalk
Write-Host "`n[3/3] Creating musetalk environment..." -ForegroundColor Cyan
& $CondaBat create -n musetalk python=3.10 -y
Set-Location "$InstallDir\MuseTalk"
& $CondaBat run -n musetalk pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118
& $CondaBat run -n musetalk pip install -r requirements.txt
& $CondaBat run -n musetalk pip install openmim
& $CondaBat run -n musetalk mim install mmengine mmcv==2.0.1 mmdet==3.1.0 mmpose==1.1.0
Write-Host "musetalk DONE" -ForegroundColor Green

Write-Host "`nAll environments created!" -ForegroundColor Green
