#!/usr/bin/env python3
"""
使用 GPT-SoVITS 生成音频
需要手动下载模型后运行
"""
import os
import sys

# 添加 GPT-SoVITS 到路径
sys.path.insert(0, 'D:/AI-Tools/GPT-SoVITS')
os.chdir('D:/AI-Tools/GPT-SoVITS')

# 读取文本
with open('D:/Project/videoremaster/outputs/ref_text.txt', 'r', encoding='utf-8') as f:
    ref_text = f.read().strip()

with open('D:/Project/videoremaster/outputs/transcripts/易经的智慧01阴阳之道.srt', 'r', encoding='utf-8') as f:
    target_text = f.read()

# 清理字幕文本
import re
lines = []
for line in target_text.split('\n'):
    # 去掉时间戳行 (00:00:00,000 --> 00:00:00,000)
    if re.match(r'^\d{2}:\d{2}:\d{2}', line):
        continue
    # 去掉数字行
    if re.match(r'^\d+$', line):
        continue
    lines.append(line)

target_text = '\n'.join(lines).strip()[:500]  # 先取前500字符

print("参考文本:", ref_text[:50])
print("目标文本:", target_text[:50])
print("\n请手动操作 GPT-SoVITS WebUI：")
print("1. 打开 http://localhost:9874")
print("2. 上传参考音频: D:/Project/videoremaster/outputs/reference.wav")
print("3. 输入参考文本:", ref_text)
print("4. 输入目标文本（复制下面内容）:")
print("-" * 50)
print(target_text)
print("-" * 50)
print("5. 点击生成音频")
