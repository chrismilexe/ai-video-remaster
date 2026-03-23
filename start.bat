@echo off
chcp 65001 >nul
echo ==========================================
echo 🎬 AI视频重制系统 - Windows控制面板
echo ==========================================
echo.

:: 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到 Python，请先安装:
    echo    https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python已安装

:: 检查依赖
echo.
echo 📦 检查依赖...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  依赖未安装，正在安装...
    pip install -r requirements.txt
)

:: 创建目录
echo 📁 创建目录...
if not exist outputs\transcripts mkdir outputs\transcripts
if not exist outputs\audio mkdir outputs\audio
if not exist outputs\videos mkdir outputs\videos
if not exist templates mkdir templates
if not exist static mkdir static

:: 启动服务
echo.
echo 🚀 启动控制面板...
echo.
echo    本地访问: http://localhost:8080
echo    按 Ctrl+C 停止服务
echo ==========================================
echo.

python app.py

pause
