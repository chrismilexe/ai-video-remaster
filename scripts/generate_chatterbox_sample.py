#!/usr/bin/env python3
"""Generate EP01 sample audio using Chatterbox TTS with English reference voice."""

import time
import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

# ── Config ──────────────────────────────────────────
REF_AUDIO = "/tmp/record_20260420.wav"
OUTPUT_DIR = "/Users/chris/Project/video2audio/outputs/audio"
OUTPUT_PREFIX = "ep01_chatterbox_sample"

# EP01 opening script (first ~90 seconds of speech)
SCRIPT = """What if the reason you feel stuck is not that life is broken, but that you keep using force where life is asking for rhythm?

Think about how most people live. When something feels uncertain, we push harder. We overthink, overwork, over-explain, and try to control the timing of everything.

And then we wonder why we feel anxious. Why relationships get tense. Why work starts draining us. Why even success can feel strangely out of sync.

So this episode is not really about learning an ancient Chinese idea just to sound wise. It is about one practical question: How do you know when to push, when to wait, and when your own energy is creating the problem?

The old language for this is Yin and Yang. But in plain English, we are talking about rhythm. Timing. Pressure and receptivity. Action and restraint."""

# ── Load model ──────────────────────────────────────
print("Loading Chatterbox Turbo model...")
model = ChatterboxTTS.from_pretrained(device="mps")
print("Model loaded.")

# ── Generate with multiple exaggeration settings ────
for exaggeration in [0.3, 0.5, 0.7]:
    print(f"\nGenerating with exaggeration={exaggeration} ...")
    start = time.time()

    wav = model.generate(
        SCRIPT,
        audio_prompt_path=REF_AUDIO,
        exaggeration=exaggeration,
        cfg_weight=0.5,
    )

    elapsed = time.time() - start
    duration = wav.shape[-1] / model.sr
    rtf = elapsed / duration

    filename = f"{OUTPUT_PREFIX}_ex{int(exaggeration*10):02d}.wav"
    filepath = f"{OUTPUT_DIR}/{filename}"
    ta.save(filepath, wav, model.sr)

    print(f"  Saved: {filename}")
    print(f"  Duration: {duration:.1f}s | Gen time: {elapsed:.1f}s | RTF: {rtf:.1f}x")
    print(f"  Sample rate: {model.sr}Hz")

print("\nAll done. Files in:", OUTPUT_DIR)
