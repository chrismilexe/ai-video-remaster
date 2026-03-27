# AI视频重制系统 - 项目状态文档

**最后更新**: 2026-03-27  
**当前分支**: main  
**项目状态**: 🟢 活跃开发中

---

## 📋 项目概览

本项目旨在将中文《易经》讲座内容转化为面向北美灵性市场的英文播客/有声书内容，并探索多语言扩展。

### 核心目标
1. 将中文《易经·阴阳之道》讲座转化为英文播客脚本
2. 使用 AI 语音克隆技术生成高质量音频
3. 制作配套视频内容（Seedance）
4. 在全球多平台分发（英语/西班牙语/德语等）

---

## ✅ 已完成任务

### 1. 内容转化 ✅
- **源文件**: `outputs/target_text.txt`（中文讲座文稿）
- **输出文件**: `scripts/target_text_english_script.md`（英文播客脚本）
- **脚本特点**:
  - 30分钟播客格式
  - 口语化、灵性导向
  - 适合北美千禧一代/Gen Z
  - 包含 [pause]、[beat] 等口播标记

### 2. 技术研究 ✅
- **AI视频生成**: Seedance 2.0（字节跳动，当前最强）
- **AI语音合成**: 
  - 商业：ElevenLabs（质量最高）、Cartesia Sonic-3（延迟最低）
  - 开源：GPT-SoVITS（推荐）、Fish Speech（Apache 2.0许可）
- **语音克隆**: 5秒-1分钟样本即可克隆声音

### 3. 分发平台调研 ✅
- 英语市场：Spotify、Audible、Apple Books、YouTube
- 西班牙语市场：Spotify拉美、Storytel
- 德语市场：Storytel（欧洲领导者）
- 香港公司入驻方案已确定可行

---

## 📁 文件结构

```
video2audio/
├── app.py                    # 主应用
├── outputs/
│   ├── target_text.txt              # 中文源文本
│   ├── target_text_english_script.txt   # 英文脚本（原位置）
│   ├── ref_text.txt
│   ├── reference.wav
│   └── transcripts/         # 字幕文件
├── scripts/                 # 新增：可提交的脚本
│   └── target_text_english_script.md    # 英文播客脚本（已同步）
├── PROJECT_STATUS.md        # 本文档
├── PROMPTS.md               # 提示词库
├── PLATFORM_GUIDE.md        # 平台分发指南
└── COMPANY_SETUP.md         # 公司入驻方案
```

---

## 🎯 下一步任务（TODO）

### 高优先级
- [ ] 录制 1-3 分钟声音样本（安静环境，WAV格式）
- [ ] 使用 GPT-SoVITS 训练个人声音模型
- [ ] 生成完整播客音频（30分钟）
- [ ] 使用 Seedance 制作配套视频

### 中优先级
- [ ] 开设 Spotify for Creators 账户（香港公司）
- [ ] 通过 INaudio 进入 Apple Books/Barnes & Noble
- [ ] ACX 税务面试（W-8BEN-E）
- [ ] 制作 YouTube 视频版本

### 低优先级（扩展）
- [ ] 西班牙语版本脚本
- [ ] 德语版本脚本
- [ ] 多语言 SEO 优化

---

## 🔧 技术栈确认

### AI语音生成（推荐方案）
```
首选: GPT-SoVITS (开源，本地部署)
- 显存要求: 4GB+ (推荐8GB)
- 训练时间: 30-60分钟
- 许可: MIT (可商用)
- 支持: 中英日粤混合

备选: ElevenLabs (商业API)
- 价格: $0.10/分钟
- 质量: 行业最高
- 无需训练，即时生成
```

### AI视频生成
```
Seedance 2.0 (字节跳动)
- 状态: 已全球发布（美国除外）
- 质量: 接近好莱坞级别
- 特点: 支持首尾帧控制、音乐同步
- 获取: 通过 CapCut 或 Dreamina 使用
```

---

## 💰 公司架构与收款

### 当前架构
- **公司**: 香港公司（已存在）
- **董事/股东**: 中国国籍（可行）
- **合伙人**: 香港身份 + 美国身份（可选增强）

### 平台入驻状态
| 平台 | 可行性 | 预扣税 | 备注 |
|------|--------|--------|------|
| ACX/Audible | ✅ 可行 | 10% | 填W-8BEN-E，香港税务居民 |
| Spotify | ⚠️ 需聚合商 | - | 通过INaudio/Author's Republic |
| Apple Books | ✅ 可行 | - | 通过聚合商 |
| YouTube | ✅ 可行 | - | 香港AdSense账户 |

### 收款路径
```
平台收入 → 香港公司账户（汇丰/中银/万里汇）→ 离岸收入（免税）
```

---

## 📚 相关文档索引

| 文档 | 路径 | 内容 |
|------|------|------|
| 英文脚本 | `scripts/target_text_english_script.md` | 完整播客脚本 |
| 提示词库 | `docs/PROMPTS.md` | 多语言转换Prompt |
| 平台指南 | `docs/PLATFORM_GUIDE.md` | 各平台入驻详情 |
| 公司方案 | `docs/COMPANY_SETUP.md` | 香港公司入驻细则 |

---

## 🔗 外部资源链接

### AI工具
- **GPT-SoVITS**: https://github.com/RVC-Boss/GPT-SoVITS
- **Seedance**: https://www.capcut.com (内置)
- **ElevenLabs**: https://elevenlabs.io

### 平台入驻
- **ACX**: https://www.acx.com
- **Spotify for Creators**: https://creators.spotify.com
- **INaudio**: https://www.in-audio.com (原Findaway)
- **Audible Tax Portal**: https://tax.audible.com

### 市场数据参考
- 全球语言服务市场 2026: $78.8B → $114.1B (2034)
- 有声书市场 CAGR: 26.4%
- Spotify Partner Program 门槛（2026.1）: 1,000听众 / 2,000小时

---

## 📝 关键决策记录

### 2026-03-27 决策
1. ✅ 确定使用 GPT-SoVITS 进行声音克隆（成本最低，效果可控）
2. ✅ 确认香港公司可直接入驻 ACX/Audible（W-8BEN-E税务身份）
3. ✅ Spotify需通过聚合商绕过（香港不在14 eligible markets）
4. ✅ 内容定位为 "Modern Spirituality" 而非 "东方玄学"（降低文化壁垒）

---

## ⚠️ 风险与注意事项

### 内容合规
- 避免使用 "治疗" "医疗" 等词汇（各国健康内容监管）
- 建议标注: "内容仅供学习参考，不构成专业建议"
- AI生成内容需在平台披露（各平台2026年新规）

### 税务合规
- 必须完成 Audible Tax Interview 才能收款
- 香港公司需按时年审（每年约3000-6000港币）
- 离岸收入需保留业务性质证明（非香港来源）

---

## 👤 项目联系信息

- **项目负责人**: [待填写]
- **香港公司**: [待填写]
- **GitHub仓库**: https://github.com/chrismilexe/ai-video-remaster

---

*本文档用于项目交接，方便其他AI助手或团队成员快速了解项目状态。*
