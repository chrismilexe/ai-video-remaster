# EP01 Audio Runbook

## Goal

Record the real status of `EP01` audio production and define the handoff into video production.

## Current State

`EP01` audio production is already complete locally.

Completed assets:

- English master script: `outputs/scripts/en/ep01_master.md`
- Sample input text: `outputs/audio/ep01_sample_input.txt`
- Full input text: `outputs/audio/ep01_full_input.txt`
- Sample TTS text: `outputs/audio/ep01_sample_tts_input.txt`
- Full TTS text: `outputs/audio/ep01_full_tts_input.txt`
- Audio manifest: `outputs/audio/ep01_audio_manifest.json`
- Preferred sample output: `outputs/audio/ep01_sample_en_ref.wav`
- Full episode audio: `outputs/audio/ep01_full.wav`

## Runtime Status

GPT-SoVITS is no longer the blocker.

Already repaired:

- CUDA and cuDNN dependency issues
- missing pretrained model assets
- `fastapi` / `starlette` version drift
- stable WebUI startup on `http://127.0.0.1:9874`

Stable local launcher:

```powershell
pwsh -File .\scripts\start_gptsovits_webui.ps1
```

## What Changed

Two different reference strategies were tested:

1. Chinese reference audio
2. New English reference audio recorded on `2026-04-20`

Current preferred result is the English-reference sample:

- `outputs/audio/ep01_sample_en_ref.wav`

The full episode render was then generated using the English reference path.

## Supporting Scripts

### Text preparation

```powershell
python .\scripts\prepare_ep01_audio.py
```

This script:

- extracts the approved body from `ep01_master.md`
- creates sample and full input text
- strips stage directions like `[pause]` and `[beat]` for TTS
- writes `outputs/audio/ep01_audio_manifest.json`

### WebUI startup

```powershell
pwsh -File .\scripts\start_gptsovits_webui.ps1
```

## Verified Result

The local full-length audio file exists:

- `outputs/audio/ep01_full.wav`

Validation snapshot:

- duration: about `578.7` seconds
- approximate runtime: `9m 39s`

## Handoff To Video

The next production step is now fixed:

1. Use `outputs/audio/ep01_full.wav` as the master narration track
2. Follow `outputs/visuals/ep01_visual_script.md` to assemble the long video
3. Use `outputs/clips/ep01_clips.md` to cut Shorts after the long video structure is stable

## Decision

`EP01` should now be treated as `audio_done`.

The main execution priority is no longer audio rendering. It is video assembly and publishing preparation.
