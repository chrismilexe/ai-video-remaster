#!/bin/bash
# 🎬 AI视频重制系统 - Mac启动脚本

echo "=========================================="
echo "🎬 AI视频重制系统 - 控制面板"
echo "=========================================="
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未检测到 Python3，请先安装:"
    echo "   https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python版本: $(python3 --version)"

# 检查依赖
echo ""
echo "📦 检查依赖..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  依赖未安装，正在安装..."
    pip3 install -r requirements.txt
fi

# 创建必要目录
echo "📁 创建目录..."
mkdir -p outputs/transcripts outputs/audio outputs/videos
mkdir -p templates static

# 启动服务
echo ""
echo "🚀 启动控制面板..."
echo ""
echo "   本地访问: http://localhost:8080"
echo "   局域网访问: http://$(ifconfig | grep "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}'):8080"
echo ""
echo "   按 Ctrl+C 停止服务"
echo "=========================================="
echo ""

python3 app.py
