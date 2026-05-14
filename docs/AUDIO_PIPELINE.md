# 音頻生成流程（Chatterbox 新版）

> 最後更新：2026-05-09
> 引擎：Chatterbox Turbo（Resemble AI, MIT 授權）
> 運行環境：Mac Apple Silicon (MPS)

## 匯率基準

DeepSeek V4 Pro 當前定價（75% 折扣，至 2026/05/31）：
- Input (cache miss): $0.435 / 1M tokens = **¥3.13 / 1M tokens**
- Output: $0.87 / 1M tokens = **¥6.26 / 1M tokens**
- Input (cache hit): $0.003625 / 1M tokens = ¥0.026 / 1M tokens

按 1 USD ≈ 7.2 CNY 換算。

---

## 完整流程（6 步）

### Step 1：中文源稿準備

| 項目 | 說明 |
|---|---|
| 做什麼 | 原始中文視頻 → WhisperX 轉錄 → 整理成中文源稿 |
| 工具 | WhisperX（4090 本地） |
| 耗時 | ~1 分鐘/小時視頻（已完成，576 個資產） |
| Token | 0（不用 LLM） |
| 空間 | ~20KB/集（transcript.srt + raw_zh.md） |
| 成本 | ¥0 |

### Step 2：英文初稿生成

| 項目 | 說明 |
|---|---|
| 做什麼 | 中文源稿 + 改寫 prompt → DeepSeek V4 Pro 生成英文初稿 |
| 工具 | DeepSeek V4 Pro API |
| Input | ~5,000 tokens（中文源稿 3K + system prompt 2K） |
| Output | ~2,500 tokens（英文初稿） |
| 耗時 | ~30 秒 |
| 空間 | ~8KB（ep01_draft.md） |
| **成本** | **¥0.032**（5K × 0.00313 + 2.5K × 0.00626） |

### Step 3：英文編輯定稿

| 項目 | 說明 |
|---|---|
| 做什麼 | AI 優化初稿 + 人工編輯（可選但建議） |
| 工具 | DeepSeek V4 Pro API + 人工 |
| Input | ~3,500 tokens（初稿 2.5K + 編輯 prompt 1K） |
| Output | ~2,500 tokens（定稿） |
| 耗時 | AI ~30 秒 + 人工 30-60 分鐘 |
| 空間 | ~8KB（ep01_master.md） |
| **成本** | **¥0.027**（AI 部分） |

### Step 4：參考音頻錄製

| 項目 | 說明 |
|---|---|
| 做什麼 | 錄製 10 秒英文男聲作為聲音克隆參考 |
| 工具 | Mac 錄音 / 手機錄音 |
| 耗時 | 1 分鐘（一次性，所有集復用） |
| 空間 | ~1MB（record_20260420.wav, 48kHz stereo） |
| 成本 | ¥0 |

### Step 5：音頻生成（Chatterbox TTS）

| 項目 | 說明 |
|---|---|
| 做什麼 | 英文定稿 → 分段生成 → 拼接成完整音頻 |
| 工具 | Chatterbox Turbo（Mac MPS 本地） |
| 段落數 | ~47 段/集（每段 2-4 句） |
| 耗時 | ~17 分鐘（7.4 分鐘音頻，RTF ≈ 2.3x） |
| Token | 0（本地，不走 API） |
| 空間 | ~40MB/集（WAV, 24000Hz 單聲道） |
| 成本 | ¥0 |

### Step 6：格式轉換

| 項目 | 說明 |
|---|---|
| 做什麼 | WAV → MP3 壓縮（供平台發布） |
| 工具 | ffmpeg |
| 耗時 | ~10 秒 |
| 空間 | ~15MB/集（MP3 320kbps）或 ~5MB（128kbps） |
| 成本 | ¥0 |

---

## 一集總計

| 維度 | 數值 |
|---|---|
| **總耗時** | 18 分鐘（不含人工編輯）；含編輯 ≈ 1 小時 |
| **LLM Token 成本** | **¥0.059**（不到 6 分錢） |
| **磁碟空間** | ~55MB/集（WAV 40MB + MP3 15MB + 文稿 20KB） |
| **需人工** | Step 3 編輯（建議 30-60 分鐘）+ Step 4 錄音（一次性） |

---

## 8 集第一季總計

| 維度 | 數值 |
|---|---|
| 總耗時（生成） | 8 × 18 分鐘 = 2.4 小時（Mac 背景跑） |
| 總耗時（含編輯） | 8 × 1 小時 ≈ 1 天 |
| LLM Token 總成本 | **¥0.47**（不到 5 毛錢） |
| 總磁碟空間 | 8 × 55MB = 440MB |

---

## 額外 AI 成本（可選）

如需 AI 輔助生成標題、簡介、短影片腳本：

| 項目 | Token | 成本/集 |
|---|---|---|
| YouTube 標題 + 簡介 + 標籤 | Input 1K + Output 800 | ¥0.008 |
| 短影片腳本（3-5 條） | Input 2K + Output 3K | ¥0.025 |
| 長影片視覺腳本 | Input 1.5K + Output 2K | ¥0.017 |
| **額外合計** | | **¥0.050/集** |

加上這些，一集 AI 成本仍不到 **¥0.11**。

---

## 成本結論

AI Token 成本可以忽略不計（一集不到 1 毛錢）。真正的成本是：
1. **人工編輯時間**（每集 30-60 分鐘）
2. **Mac 生成等待**（每集 10-17 分鐘，可背景跑）
3. **磁碟空間**（每集 15-40MB）

---

## 批次生產記錄（2026-05-08 ~ 05-09）

| # | 標籤 | 檔案 | 大小 | 段數 | 耗時 |
|---|---|---|---|---|---|
| 1 | EP01 | ep01_full_chatterbox.wav | 40MB | 47 | 17 分 |
| 2 | EP02 | ep02_full_chatterbox.wav | 38MB | 33 | 15 分 |
| 3 | EP03 | ep03_full_chatterbox.wav | 37MB | 34 | 15 分 |
| 4 | EP04 | ep04_full_chatterbox.wav | 32MB | 28 | 13 分 |
| 5 | RADAR01 | radar01_full_chatterbox.wav | 15MB | 12 | 7 分 |
| 6 | RADAR02 | radar02_full_chatterbox.wav | 22MB | 19 | 10 分 |
| 7 | CASE01 | case01_full_chatterbox.wav | 24MB | 25 | 10 分 |
| 8 | TRUMP | trump_full_chatterbox.wav | 31MB | 30 | 13 分 |

**合計：239MB，約 55 分鐘音頻，總生成耗時 ~100 分鐘**

## 生成腳本

| 腳本 | 用途 |
|---|---|
| `scripts/generate_chatterbox_sample.py` | 單集樣音生成（多個 exaggeration 對比） |
| `scripts/generate_ep01_full.py` | EP01 完整生成（單段，已廢棄） |
| `scripts/generate_ep01_chunked.py` | EP01 分段生成 + 拼接 |
| `scripts/generate_all_episodes.py` | 批次生成全部集數 |
