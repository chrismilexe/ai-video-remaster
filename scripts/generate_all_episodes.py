#!/usr/bin/env python3
"""Batch generate all available episodes using Chatterbox TTS."""

import time
import re
import torch
import torchaudio as ta
from pathlib import Path
from chatterbox.tts import ChatterboxTTS

REF_AUDIO = "/tmp/record_20260420.wav"
SCRIPTS_DIR = "/Users/chris/Project/video2audio/outputs/scripts/en"
OUTPUT_DIR = "/Users/chris/Project/video2audio/outputs/audio"
EXAGGERATION = 0.5

EPISODES = [
    {"file": "ep02_master.md", "label": "EP02", "script_marker": "# English Script"},
    {"file": "ep03_master.md", "label": "EP03", "script_marker": "# English Script"},
    {"file": "ep04_master.md", "label": "EP04", "script_marker": "# English Script"},
    {"file": "outcome_radar_01_when_pressure_stops_working.md", "label": "RADAR01", "script_marker": "## Script"},
    {"file": "outcome_radar_02_when_identity_costs_the_business.md", "label": "RADAR02", "script_marker": "## Script"},
    {"file": "pattern_case_01_what_happens_when_power_loses_balance.md", "label": "CASE01", "script_marker": "## Script"},
    {"file": "trump_yinyang_hot_take.md", "label": "TRUMP", "script_marker": "## Script"},
]

def parse_script(filepath, script_marker):
    """Extract clean English script from markdown file."""
    with open(filepath, "r") as f:
        content = f.read()

    # Find script section
    idx = content.find(script_marker)
    if idx == -1:
        # Fallback: find any "Script" header
        for marker in ["# English Script", "## Script", "# Script"]:
            idx = content.find(marker)
            if idx != -1:
                break
    if idx == -1:
        raise ValueError(f"Could not find script section in {filepath}")

    script = content[idx:]

    # Remove header line
    script = script.split("\n", 1)[1] if "\n" in script else script

    # Remove markdown headers, reading notes, metadata lines
    lines = []
    for line in script.split("\n"):
        line = line.strip()
        if not line:
            lines.append("")
            continue
        # Skip markdown headers and metadata
        if line.startswith("#") or line.startswith("---"):
            continue
        # Skip reading notes
        if line.startswith("- ") and ("feel" in line.lower() or "delivery" in line.lower() or "rhythm" in line.lower() or "emphasis" in line.lower() or "avoid" in line.lower()):
            continue
        lines.append(line)

    script = "\n".join(lines)

    # Remove [pause], [beat] markers
    script = re.sub(r'\[pause\]', '', script)
    script = re.sub(r'\[beat\]', '', script)

    # Collapse multiple blank lines
    script = re.sub(r'\n{3,}', '\n\n', script)
    script = script.strip()

    # Split into paragraphs (by double newline)
    paragraphs = [p.strip() for p in script.split("\n\n") if p.strip()]

    # Merge very short paragraphs with neighbors for better audio flow
    merged = []
    for p in paragraphs:
        # If paragraph is very short (< 100 chars), merge with previous
        if len(p) < 100 and merged:
            merged[-1] = merged[-1] + ". " + p
        else:
            merged.append(p)

    return merged


def generate_episode(model, label, paragraphs, output_dir):
    """Generate audio for a single episode from paragraphs."""
    print(f"\n{'='*60}")
    print(f"  {label}: {len(paragraphs)} paragraphs")
    print(f"{'='*60}")

    chunks = []
    total_dur = 0.0
    t_start = time.time()

    silence = torch.zeros(1, int(0.5 * model.sr))

    for i, para in enumerate(paragraphs):
        t0 = time.time()
        try:
            wav = model.generate(para, audio_prompt_path=REF_AUDIO, exaggeration=EXAGGERATION, cfg_weight=0.5)
        except Exception as e:
            print(f"  [{i+1}/{len(paragraphs)}] ERROR: {e}, retrying with shorter text...")
            # If too long, split further
            sentences = re.split(r'(?<=[.!?])\s+', para)
            mid = len(sentences) // 2
            part1 = " ".join(sentences[:mid])
            part2 = " ".join(sentences[mid:])
            wav1 = model.generate(part1, audio_prompt_path=REF_AUDIO, exaggeration=EXAGGERATION, cfg_weight=0.5)
            wav2 = model.generate(part2, audio_prompt_path=REF_AUDIO, exaggeration=EXAGGERATION, cfg_weight=0.5)
            wav = torch.cat([wav1, wav2], dim=-1)

        dur = wav.shape[-1] / model.sr
        chunks.append(wav)
        if i < len(paragraphs) - 1:
            chunks.append(silence)
        total_dur += dur
        elapsed = time.time() - t0
        preview = para[:50].replace("\n", " ")
        print(f"  [{i+1:02d}/{len(paragraphs)}] {dur:.1f}s ({elapsed:.0f}s) | {preview}...")

    print(f"\n  Concatenating {len(chunks)} chunks...")
    full_wav = torch.cat(chunks, dim=-1)
    total_dur = full_wav.shape[-1] / model.sr

    filename = f"{label.lower()}_full_chatterbox.wav"
    filepath = f"{output_dir}/{filename}"
    ta.save(filepath, full_wav, model.sr)

    total_time = time.time() - t_start
    print(f"  Done: {filename}")
    print(f"  Duration: {total_dur:.1f}s ({total_dur/60:.1f}min)")
    print(f"  Time: {total_time:.0f}s ({total_time/60:.1f}min)")
    return total_dur, total_time


def main():
    print("Loading Chatterbox Turbo...")
    model = ChatterboxTTS.from_pretrained(device="mps")

    grand_start = time.time()
    results = []

    for ep in EPISODES:
        filepath = Path(SCRIPTS_DIR) / ep["file"]
        if not filepath.exists():
            print(f"\nSKIP {ep['label']}: file not found: {filepath}")
            continue

        paragraphs = parse_script(str(filepath), ep["script_marker"])
        print(f"\n{ep['label']}: {len(paragraphs)} paragraphs from {filepath.name}")

        dur, gen_time = generate_episode(model, ep["label"], paragraphs, OUTPUT_DIR)
        results.append({"label": ep["label"], "duration": dur, "time": gen_time})

    grand_total = time.time() - grand_start
    total_dur = sum(r["duration"] for r in results)
    total_gen = sum(r["time"] for r in results)

    print(f"\n{'='*60}")
    print(f"  ALL DONE")
    print(f"{'='*60}")
    for r in results:
        print(f"  {r['label']}: {r['duration']:.0f}s ({r['duration']/60:.1f}min) | gen: {r['time']:.0f}s")
    print(f"  ---")
    print(f"  Total audio: {total_dur:.0f}s ({total_dur/60:.1f}min)")
    print(f"  Total gen time: {total_gen:.0f}s ({total_gen/60:.1f}min)")
    print(f"  Wall time: {grand_total:.0f}s ({grand_total/60:.1f}min)")

if __name__ == "__main__":
    main()
