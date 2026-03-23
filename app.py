#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 AI视频重制系统 - 统一控制面板
在 Mac 上运行，控制远程 4090 工作站或本地执行
"""

import os
import sys
import json
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, jsonify, request, send_file
from flask_socketio import SocketIO, emit

# ============== 配置区域 ==============
CONFIG = {
    "remote_host": "192.168.1.100",  # 修改为你的4090电脑IP
    "remote_user": "user",           # 修改为你的用户名
    "use_remote": False,             # True=远程控制, False=本地运行(如果Mac有显卡)
    "tools_dir": "D:/\AI-Tools" if sys.platform == "win32" else "~/AI-Tools",
    "output_dir": "./outputs",
}

# 工具配置
TOOLS = {
    "whisperx": {
        "name": "🎤 WhisperX 语音转文字",
        "description": "将视频/音频转换为带时间戳的文字稿，支持说话人分离",
        "conda_env": "whisperx",
        "port": None,
        "install_cmd": "conda create -n whisperx python=3.10 -y && conda activate whisperx && pip install torch==2.5.1 torchvision==2.5.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124 && pip install whisperx",
        "models": ["tiny", "base", "small", "medium", "large-v3", "large-v3-turbo"],
        "default_model": "large-v3",
        "vram_gb": 10,
    },
    "gptsovits": {
        "name": "🗣️ GPT-SoVITS 声音克隆",
        "description": "中文声音克隆首选，5秒样本即可克隆声音",
        "conda_env": "gptsovits",
        "port": 9874,
        "url": "http://localhost:9874",
        "install_cmd": "conda create -n gptsovits python=3.10 -y && conda activate gptsovits && git clone https://github.com/RVC-Boss/GPT-SoVITS.git && cd GPT-SoVITS && powershell -ExecutionPolicy ByPass -File install.ps1 --Device CU124 --Source HF",
        "models": ["默认模型"],
        "default_model": "默认模型",
        "vram_gb": 12,
    },
    "cosyvoice": {
        "name": "🎙️ CosyVoice 阿里TTS",
        "description": "阿里出品，支持流式输出，150ms低延迟",
        "conda_env": "cosyvoice",
        "port": 8000,
        "url": "http://localhost:8000",
        "install_cmd": "conda create -n cosyvoice python=3.10 -y && conda activate cosyvoice && git clone https://github.com/FunAudioLLM/CosyVoice.git && cd CosyVoice && pip install -r requirements.txt && pip install -e .",
        "models": ["CosyVoice-300M", "CosyVoice-300M-SFT", "CosyVoice-300M-Instruct"],
        "default_model": "CosyVoice-300M",
        "vram_gb": 8,
    },
    "fishspeech": {
        "name": "🐟 Fish Speech",
        "description": "多语言支持，Apache 2.0许可可商用",
        "conda_env": "fishspeech",
        "port": 7860,
        "url": "http://localhost:7860",
        "install_cmd": "conda create -n fishspeech python=3.10 -y && conda activate fishspeech && git clone https://github.com/fishaudio/fish-speech.git && cd fish-speech && pip install -e .",
        "models": ["fish-speech-1.5"],
        "default_model": "fish-speech-1.5",
        "vram_gb": 8,
    },
    "musetalk": {
        "name": "👄 MuseTalk 对口型",
        "description": "实时高质量对口型，30fps流畅生成",
        "conda_env": "musetalk",
        "port": None,
        "install_cmd": "conda create -n musetalk python=3.10 -y && conda activate musetalk && git clone https://github.com/TMElyralab/MuseTalk.git && cd MuseTalk && pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118 && pip install -r requirements.txt && pip install openmim && mim install mmengine mmcv==2.0.1 mmdet==3.1.0 mmpose==1.1.0",
        "models": ["默认模型"],
        "default_model": "默认模型",
        "vram_gb": 8,
    },
    "videoretalking": {
        "name": "🎥 VideoReTalking",
        "description": "后处理级对口型，质量最高但速度较慢",
        "conda_env": "retalking",
        "port": None,
        "install_cmd": "conda create -n retalking python=3.8 -y && conda activate retalking && git clone https://github.com/OpenTalker/video-retalking.git && cd video-retalking && pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113 && pip install -r requirements.txt",
        "models": ["默认模型"],
        "default_model": "默认模型",
        "vram_gb": 8,
    },
    "ollama": {
        "name": "🧠 Ollama 本地LLM",
        "description": "运行本地大模型，用于文稿优化和翻译",
        "conda_env": None,
        "port": 11434,
        "url": "http://localhost:11434",
        "install_cmd": "# Windows: 下载安装包 https://ollama.com/download\\n# Linux: curl -fsSL https://ollama.com/install.sh | sh",
        "models": ["qwen2.5:32b", "llama3.3:70b", "deepseek-v3", "phi4"],
        "default_model": "qwen2.5:32b",
        "vram_gb": 20,
    },
}

# ============== Flask 应用 ==============
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ai-video-remaster-2026'
socketio = SocketIO(app, cors_allowed_origins="*")

# 进程管理
running_processes = {}
process_logs = {}

# ============== 工具函数 ==============

def get_conda_path():
    """获取conda路径"""
    if sys.platform == "win32":
        return os.path.expanduser("~/miniconda3/Scripts/conda.exe")
    else:
        return "conda"

def run_command(cmd, tool_id=None, cwd=None):
    """在后台运行命令并实时输出日志"""
    def target():
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=cwd,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if tool_id:
            running_processes[tool_id] = process
            process_logs[tool_id] = []
        
        for line in process.stdout:
            line = line.strip()
            if tool_id:
                process_logs[tool_id].append({
                    'time': datetime.now().strftime('%H:%M:%S'),
                    'message': line
                })
                socketio.emit(f'log_{tool_id}', {'message': line})
        
        process.wait()
        if tool_id and tool_id in running_processes:
            del running_processes[tool_id]
    
    thread = threading.Thread(target=target)
    thread.start()
    return thread

def check_tool_status(tool_id):
    """检查工具是否已安装和运行中"""
    tool = TOOLS[tool_id]
    status = {
        'installed': False,
        'running': False,
        'port_open': False,
        'pid': None
    }
    
    # 检查conda环境是否存在
    if tool_id == 'ollama':
        # Ollama 是系统级安装
        result = subprocess.run(['which', 'ollama'], capture_output=True)
        status['installed'] = result.returncode == 0
    else:
        result = subprocess.run(['conda', 'env', 'list'], capture_output=True, text=True)
        status['installed'] = tool['conda_env'] in result.stdout
    
    # 检查端口是否被占用
    if tool['port']:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', tool['port']))
        status['port_open'] = result == 0
        sock.close()
        status['running'] = status['port_open']
    
    return status

# ============== 路由 ==============

@app.route('/')
def index():
    """主页面"""
    # 检查各工具状态
    tool_status = {k: check_tool_status(k) for k in TOOLS.keys()}
    return render_template('index.html', tools=TOOLS, status=tool_status)

@app.route('/api/tools')
def get_tools():
    """获取工具列表"""
    return jsonify(TOOLS)

@app.route('/api/status/<tool_id>')
def get_status(tool_id):
    """获取指定工具状态"""
    if tool_id not in TOOLS:
        return jsonify({'error': 'Tool not found'}), 404
    return jsonify(check_tool_status(tool_id))

@app.route('/api/install/<tool_id>', methods=['POST'])
def install_tool(tool_id):
    """安装工具"""
    if tool_id not in TOOLS:
        return jsonify({'error': 'Tool not found'}), 404
    
    tool = TOOLS[tool_id]
    
    if tool_id == 'ollama':
        # Ollama 特殊处理
        return jsonify({'error': '请手动下载安装包: https://ollama.com/download'}), 400
    
    # 执行安装命令
    cmd = tool['install_cmd']
    run_command(cmd, tool_id=f"{tool_id}_install")
    
    return jsonify({'message': f'开始安装 {tool["name"]}', 'tool_id': tool_id})

@app.route('/api/start/<tool_id>', methods=['POST'])
def start_tool(tool_id):
    """启动工具服务"""
    if tool_id not in TOOLS:
        return jsonify({'error': 'Tool not found'}), 404
    
    tool = TOOLS[tool_id]
    status = check_tool_status(tool_id)
    
    if status['running']:
        return jsonify({'message': f'{tool["name"]} 已在运行', 'url': tool.get('url')})
    
    # 构建启动命令
    if tool_id == 'whisperx':
        cmd = f"conda activate {tool['conda_env']} && whisperx --help"
    elif tool_id == 'gptsovits':
        cmd = f"cd {CONFIG['tools_dir']}/GPT-SoVITS && conda activate {tool['conda_env']} && python webui.py"
    elif tool_id == 'cosyvoice':
        cmd = f"cd {CONFIG['tools_dir']}/CosyVoice && conda activate {tool['conda_env']} && python webui.py"
    elif tool_id == 'fishspeech':
        cmd = f"cd {CONFIG['tools_dir']}/fish-speech && conda activate {tool['conda_env']} && python -m fish_speech.webui"
    elif tool_id == 'musetalk':
        cmd = f"cd {CONFIG['tools_dir']}/MuseTalk && conda activate {tool['conda_env']}"
        return jsonify({'message': 'MuseTalk 是命令行工具，请使用"运行推理"功能'})
    elif tool_id == 'videoretalking':
        cmd = f"cd {CONFIG['tools_dir']}/video-retalking && conda activate {tool['conda_env']}"
        return jsonify({'message': 'VideoReTalking 是命令行工具，请使用"运行推理"功能'})
    elif tool_id == 'ollama':
        cmd = "ollama serve"
    else:
        return jsonify({'error': '未知的工具类型'}), 400
    
    run_command(cmd, tool_id)
    
    time.sleep(2)  # 等待启动
    status = check_tool_status(tool_id)
    
    return jsonify({
        'message': f'{tool["name"]} 启动中...',
        'url': tool.get('url'),
        'running': status['running']
    })

@app.route('/api/stop/<tool_id>', methods=['POST'])
def stop_tool(tool_id):
    """停止工具服务"""
    if tool_id in running_processes:
        process = running_processes[tool_id]
        process.terminate()
        del running_processes[tool_id]
        return jsonify({'message': f'{TOOLS[tool_id]["name"]} 已停止'})
    
    # 尝试通过端口查找并kill
    tool = TOOLS.get(tool_id)
    if tool and tool['port']:
        if sys.platform == "win32":
            cmd = f"for /f \"tokens=5\" %a in ('netstat -ano ^| findstr :{tool[\"port\"]}') do taskkill /F /PID %a"
        else:
            cmd = f"lsof -ti:{tool['port']} | xargs kill -9"
        subprocess.run(cmd, shell=True)
    
    return jsonify({'message': f'{tool["name"]} 停止命令已发送'})

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    """执行语音转文字"""
    data = request.json
    video_path = data.get('video_path', '')
    model = data.get('model', 'large-v3')
    language = data.get('language', 'zh')
    diarize = data.get('diarize', True)
    
    if not video_path or not os.path.exists(video_path):
        return jsonify({'error': '视频文件不存在'}), 400
    
    output_dir = data.get('output_dir', './outputs/transcripts')
    os.makedirs(output_dir, exist_ok=True)
    
    cmd = f"conda activate whisperx && whisperx \"{video_path}\" --model {model} --language {language}"
    if diarize:
        cmd += " --diarize"
    cmd += f" --output_dir \"{output_dir}\" --output_format srt"
    
    run_command(cmd, tool_id='transcribe')
    
    return jsonify({
        'message': '开始转录',
        'command': cmd,
        'output_dir': output_dir
    })

@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    """执行文字转语音"""
    data = request.json
    text = data.get('text', '')
    tool_id = data.get('tool', 'gptsovits')
    voice_sample = data.get('voice_sample', '')
    
    if not text:
        return jsonify({'error': '文本不能为空'}), 400
    
    output_dir = data.get('output_dir', './outputs/audio')
    os.makedirs(output_dir, exist_ok=True)
    
    # 根据工具构建命令
    if tool_id == 'gptsovits':
        # GPT-SoVITS 需要通过API调用
        return jsonify({
            'message': '请使用 GPT-SoVITS WebUI 进行声音克隆',
            'url': 'http://localhost:9874'
        })
    elif tool_id == 'cosyvoice':
        return jsonify({
            'message': '请使用 CosyVoice WebUI 生成语音',
            'url': 'http://localhost:8000'
        })
    elif tool_id == 'fishspeech':
        return jsonify({
            'message': '请使用 FishSpeech WebUI 生成语音',
            'url': 'http://localhost:7860'
        })
    
    return jsonify({'error': '未知的TTS工具'}), 400

@app.route('/api/lipsync', methods=['POST'])
def lip_sync():
    """执行对口型"""
    data = request.json
    video_path = data.get('video_path', '')
    audio_path = data.get('audio_path', '')
    tool_id = data.get('tool', 'musetalk')
    
    if not video_path or not audio_path:
        return jsonify({'error': '视频和音频路径不能为空'}), 400
    
    output_dir = data.get('output_dir', './outputs/videos')
    os.makedirs(output_dir, exist_ok=True)
    
    output_name = f"lipsync_{int(time.time())}.mp4"
    output_path = os.path.join(output_dir, output_name)
    
    if tool_id == 'musetalk':
        cmd = f"cd {CONFIG['tools_dir']}/MuseTalk && conda activate musetalk && python inference.py --video_path \"{video_path}\" --audio_path \"{audio_path}\" --output_path \"{output_path}\""
    elif tool_id == 'videoretalking':
        cmd = f"cd {CONFIG['tools_dir']}/video-retalking && conda activate retalking && python inference.py --face \"{video_path}\" --audio \"{audio_path}\" --outfile \"{output_path}\""
    else:
        return jsonify({'error': '未知的对口型工具'}), 400
    
    run_command(cmd, tool_id='lipsync')
    
    return jsonify({
        'message': '开始对口型合成',
        'output_path': output_path
    })

@app.route('/api/workflow', methods=['POST'])
def run_workflow():
    """执行完整工作流"""
    data = request.json
    video_path = data.get('video_path', '')
    
    if not video_path:
        return jsonify({'error': '视频路径不能为空'}), 400
    
    # 创建工作流脚本
    workflow_id = f"workflow_{int(time.time())}"
    output_base = f"./outputs/{workflow_id}"
    os.makedirs(output_base, exist_ok=True)
    
    workflow_script = f"""
# AI视频重制工作流
# 输入: {video_path}
# 输出: {output_base}

echo "=== 步骤1: 语音转文字 ==="
conda activate whisperx
whisperx "{video_path}" --model large-v3 --language zh --diarize --output_dir "{output_base}/transcript" --output_format srt

echo "=== 步骤2: 等待用户编辑文稿 ==="
echo "请编辑 {output_base}/transcript 中的字幕文件，然后继续"

echo "=== 步骤3: 声音克隆 (需要手动在WebUI中操作) ==="
echo "打开 http://localhost:9874 进行声音克隆"

echo "=== 步骤4: 对口型 (需要手动在WebUI中操作) ==="
echo "使用生成的音频和原视频进行对口型"

echo "=== 完成 ==="
"""
    
    script_path = f"{output_base}/workflow.sh"
    with open(script_path, 'w') as f:
        f.write(workflow_script)
    
    return jsonify({
        'message': '工作流已创建',
        'workflow_id': workflow_id,
        'output_base': output_base,
        'script_path': script_path,
        'steps': [
            '转录视频生成字幕',
            '手动编辑字幕文件',
            '使用GPT-SoVITS克隆声音并生成音频',
            '使用MuseTalk对口型'
        ]
    })

@app.route('/api/logs/<tool_id>')
def get_logs(tool_id):
    """获取工具日志"""
    return jsonify(process_logs.get(tool_id, []))

@app.route('/api/outputs')
def list_outputs():
    """列出所有输出文件"""
    outputs = {
        'transcripts': [],
        'audio': [],
        'videos': []
    }
    
    for category in outputs.keys():
        dir_path = f"./outputs/{category}"
        if os.path.exists(dir_path):
            outputs[category] = [
                {'name': f, 'path': os.path.join(dir_path, f), 'size': os.path.getsize(os.path.join(dir_path, f))}
                for f in os.listdir(dir_path)
            ]
    
    return jsonify(outputs)

# ============== 模板 ==============

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_file(f'./static/{filename}')

# ============== 主入口 ==============

if __name__ == '__main__':
    os.makedirs('./outputs', exist_ok=True)
    os.makedirs('./templates', exist_ok=True)
    os.makedirs('./static', exist_ok=True)
    
    print("=" * 60)
    print("🎬 AI视频重制系统 - 控制面板")
    print("=" * 60)
    print(f"访问地址: http://localhost:8080")
    print("按 Ctrl+C 停止服务")
    print("=" * 60)
    
    socketio.run(app, host='0.0.0.0', port=8080, debug=False)
