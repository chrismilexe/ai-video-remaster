# Windows 11 批量入库执行手册

这份手册是给家里的 `Windows 11 + RTX 4090` 机器使用的。

目标：
- 从 GitHub 拉取本仓库最新代码
- 配置本地内容库目录
- 批量把视频转成中文文稿资产
- 为后续主题总稿和英文生成准备基础库

---

## 1. 首次准备

确认以下条件已经满足：

- 已安装 Miniconda，默认路径为 `%USERPROFILE%\miniconda3`
- 已创建 `whisperx` conda 环境
- `whisperx` 在该环境内可运行
- 仓库已同步到本地，例如 `D:\Project\video2audio`

如环境还没装好，先运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\deploy.ps1
```

---

## 2. 拉取最新代码

在仓库根目录执行：

```powershell
git pull origin main
```

---

## 3. 准备本地配置

首次执行时复制配置文件：

```powershell
Copy-Item .\config\library.example.json .\config\library.json
```

默认内容库根目录：

```text
D:\Video2AudioLibrary
```

默认待处理目录：

```text
D:\Video2AudioLibrary\incoming
```

如需修改路径，编辑：

```text
config\library.json
```

---

## 4. 放入待处理视频

把要转录的视频或音频放进：

```text
D:\Video2AudioLibrary\incoming
```

支持递归扫描子目录。

---

## 5. 执行批量入库

标准模式：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_batch_ingest.ps1
```

快速试跑：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_batch_ingest.ps1 --fast --limit 5
```

强制重跑：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_batch_ingest.ps1 --force
```

开启说话人分离：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_batch_ingest.ps1 --diarize
```

注意：
- `--diarize` 需要在 `config\library.json` 里配置 `hf_token`
- 默认不开启 diarization
- 默认模型是 `large-v3`
- `--fast` 会切到 `large-v3-turbo`

---

## 6. 预期输出

每条资产会写到：

```text
D:\Video2AudioLibrary\assets\<asset_id>\
```

其中至少包含：

- `transcript.srt`
- `transcript.json`
- `raw_zh.md`
- `metadata.json`

全库索引在：

```text
D:\Video2AudioLibrary\manifests\library_index.jsonl
```

---

## 7. 完成后检查

至少检查这几项：

1. `library_index.jsonl` 有新增记录
2. `assets\<asset_id>\raw_zh.md` 可以正常打开并看到中文文稿
3. `assets\<asset_id>\transcript.srt` 时间戳正常
4. 同一文件再次运行时会被跳过，而不是重复入库

---

## 8. 常见问题

### 1. 找不到 conda

确认：

```text
%USERPROFILE%\miniconda3\condabin\conda.bat
```

存在。

### 2. `whisperx` 环境不存在

重新执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\setup-envs.ps1
```

### 3. 显存不足

可先试：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_batch_ingest.ps1 --fast --limit 2
```

或把 `config\library.json` 中的 `batch_size` 调小。

### 4. 需要重做某批资产

使用：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_batch_ingest.ps1 --force
```

---

## 9. 下一步

完成批量入库后，后续工作基于这些产物继续：

- 单视频清稿
- 主题归并
- 中文主题总稿
- 英文长篇主稿
- 时事简报结合创作
