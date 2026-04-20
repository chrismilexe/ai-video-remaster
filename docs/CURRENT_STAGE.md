# 当前阶段说明

**最后更新**: 2026-04-21

## 1. 项目现在到哪一步了

项目已经不再停留在“内容研究”或“脚本准备”阶段。

当前真实阶段是：

`中文素材库存 -> 英文主稿 -> 英文长音频` 这条链已经跑通，正在进入 `长视频装配` 阶段。

换句话说，现阶段最关键的事情已经不是继续讨论选题，而是把已经完成的 `EP01` 做成可发布的音频和视频成品。

## 2. 已完成内容

### 内容资产

- 中文素材库已经建立，`library/assets/` 下有批量转录资产
- `EP01` 英文主稿已完成：`outputs/scripts/en/ep01_master.md`
- `EP01` 短视频脚本已完成：`outputs/clips/ep01_clips.md`
- `EP01` 长视频视觉脚本已完成：`outputs/visuals/ep01_visual_script.md`
- `EP01` 发布包已完成：`outputs/publishing/ep01_youtube_launch_pack.md`

### 音频生产链

- GPT-SoVITS 本地环境已经修复并可稳定启动
- 文本预处理脚本已补齐：`scripts/prepare_ep01_audio.py`
- WebUI 启动脚本已补齐：`scripts/start_gptsovits_webui.ps1`
- `EP01` 样音已生成完成
- `EP01` 整集长音频已生成完成

## 3. 当前关键产物

### 已提交到仓库的可追踪文件

- 当前阶段文档：`docs/CURRENT_STAGE.md`
- 音频执行说明：`docs/EP01_AUDIO_RUNBOOK.md`
- 生产脚本：`scripts/prepare_ep01_audio.py`
- 启动脚本：`scripts/start_gptsovits_webui.ps1`
- 音频清单：`outputs/audio/ep01_audio_manifest.json`

### 本地产物

以下文件已经在本地生成，可直接用于后续制作：

- `outputs/audio/ep01_sample_en_ref.wav`
- `outputs/audio/ep01_full.wav`

说明：

- 仓库默认忽略 `.wav`、`.mp3`、`.mp4` 等大体积输出文件
- 原始英文参考录音属于个人素材，也默认只保留在本地，不随 GitHub 同步

## 4. 当前判断

项目最大的阻塞已经不是：

- 没有内容
- 没有脚本
- 没有 TTS 环境

当前真正的下一步是：

1. 用 `outputs/audio/ep01_full.wav` + `outputs/visuals/ep01_visual_script.md` 装配 `EP01` 长视频
2. 从 `EP01` 长音频和脚本里切出 3-5 条 Shorts
3. 核对标题、描述、封面与发布包，准备首发

## 5. 当前优先级

### P0

- 产出 `EP01` 长视频成品

### P1

- 产出 `EP01` Shorts
- 完成 `EP01` 发布前检查

### P2

- 把 `EP02` 推进到英文主稿
- 复用 `EP01` 音频 SOP 到后续集数

## 6. 不该优先做的事

现阶段不应优先继续投入：

- 大量补写战略文档
- 再做一轮宽泛平台研究
- 继续扩展工具栈
- 在 `EP01` 未视频化前跳到 `EP04+` 的脚本生产

原因很简单：当前最短路径是先把已经完成 80% 的 `EP01` 变成真正可上线的成品。
