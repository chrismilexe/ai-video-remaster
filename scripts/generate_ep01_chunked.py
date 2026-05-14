#!/usr/bin/env python3
"""Generate full EP01 audio in chunks, then concatenate."""

import time
import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

REF_AUDIO = "/tmp/record_20260420.wav"
OUTPUT_DIR = "/Users/chris/Project/video2audio/outputs/audio"
EXAGGERATION = 0.5

# Split into natural paragraphs for chunked generation
PARAGRAPHS = [
    "What if the reason you feel stuck is not that life is broken, but that you keep using force where life is asking for rhythm?",

    "Think about how most people live. When something feels uncertain, we push harder. We overthink, overwork, over-explain, and try to control the timing of everything.",

    "And then we wonder why we feel anxious. Why relationships get tense. Why work starts draining us. Why even success can feel strangely out of sync.",

    "So this episode is not really about learning an ancient Chinese idea just to sound wise. It is about one practical question: How do you know when to push, when to wait, and when your own energy is creating the problem?",

    "The old language for this is Yin and Yang. But in plain English, we are talking about rhythm. Timing. Pressure and receptivity. Action and restraint.",

    "And what this means in real life is simple. If you do not understand the rhythm of a moment, you will keep using the wrong energy. You will push when you need to listen. You will wait when you need to move.",

    "That is where a lot of suffering begins. Not always from danger. Sometimes from misalignment. From trying to make life obey a tempo it was never in.",

    "When people first hear about the I Ching, they often assume it is just an old book of symbols. Ancient. Mystical. Interesting, maybe. But not something that could actually help you live better on a Tuesday afternoon.",

    "But the real question is not, what is this book. The real question is, what did these people notice about life that we keep forgetting.",

    "They noticed that nothing stays in one state forever. Everything shifts. Everything turns. Everything carries the seed of change inside itself.",

    "Day turns into night. Energy turns into fatigue. Closeness turns into distance. Confidence turns into doubt.",

    "And right here is the first turning point. Most people do not suffer because life changes. They suffer because they keep demanding stability from a world that is built on movement.",

    "That is why balance is not something you achieve once. Balance is something you keep adjusting. Again and again. Moment by moment.",

    "A simple way to practice this is to stop asking, how do I stay in control. And start asking, what is this moment asking for.",

    "That one shift changes a lot. Because control and clarity are not the same thing. You can be highly controlling and still be completely out of touch with reality.",

    "Think about relationships. Sometimes we feel distance and immediately try to fix it. We text more. Explain more. Push for resolution faster. We call that effort. We call that care.",

    "But sometimes that effort is actually pressure. Sometimes the other person does not need more force. They need more space. More calm. Better timing.",

    "Too much force breaks connection. Too much retreat creates distance. And balance is not choosing one side forever. It is sensing what the relationship needs now.",

    "That is a practical version of Yin and Yang. One movement reaches outward. One movement receives. One movement acts. One movement allows.",

    "Neither one is the villain. The problem begins when we get trapped in only one mode.",

    "Now let me turn the lens a little. Because if this only applied to relationships, it would still be useful. But it applies everywhere.",

    "It shows up at work. A lot of people are praised for relentless output. Keep going. Keep building. Keep pushing. Keep performing.",

    "And for a while, that energy works. Until it does not. Until your body starts resisting the life your ambition designed.",

    "What we call burnout is often an argument with rhythm. You keep demanding expansion when your system is asking for recovery. You keep trying to produce when life is asking you to reset.",

    "And here is the second turning point. A lot of people hear that and think, so I should just stop trying. No. That is not the point.",

    "This is not a call to become passive. It is a call to become accurate. Sustainable power is rhythmic. Not constant.",

    "Breathing works because you inhale and exhale. Walking works because one foot leaves the ground while the other supports you. Even strength training works through stress and recovery.",

    "So why do we expect emotional life to work differently. Why do we think maturity means always being composed, always certain, always moving forward.",

    "A question to sit with is this: Where in your life are you trying to stay in one mode for too long.",

    "Too strong for too long. Too available for too long. Too guarded for too long. Too productive for too long. Too cautious for too long.",

    "Every one of those can become imbalance. Even a good quality becomes distortion when it loses rhythm.",

    "This is also why decision-making becomes so hard. A lot of people think clarity comes from squeezing harder. More analysis. More research. More mental pressure.",

    "But often clarity shows up after pressure drops. After the noise calms. After you stop trying to force certainty from a mind that is already overloaded.",

    "And this is the third turning point. Not every problem gets solved by more effort. Some problems get solved by better timing.",

    "Some decisions improve through observation. Some through distance. Some through one night of sleep. Some through one honest conversation.",

    "That does not sound dramatic. But it is powerful. Because pressure is often a terrible substitute for timing.",

    "This is why ancient wisdom still matters. Not because old symbols are magical. But because human beings keep repeating the same mistake. We confuse force with intelligence. We confuse motion with progress. We confuse control with alignment.",

    "So if you want one practical takeaway from this episode, let it be this: Before you push harder, ask what kind of movement this moment actually needs.",

    "Does it need effort. Does it need patience. Does it need honesty. Does it need rest. Does it need a boundary. Does it need one clear step instead of ten frantic ones.",

    "Tonight, try this. Choose one area of your life that feels tense right now. A relationship. A decision. Your work. Your body. Your future.",

    "Write down three short answers. Where am I forcing. Where am I withdrawing. What would balance look like here for just the next seven days.",

    "Not forever. Not for the rest of your life. Just the next seven days. Because balance becomes real when it becomes specific.",

    "And that is the deeper point. Yin and Yang is not a decorative concept. It is a way of seeing movement, tension, and change more accurately.",

    "Life is rarely asking you to become one fixed thing. It is asking you to respond intelligently as conditions change.",

    "Balance is not fifty-fifty. Balance is knowing what the moment asks for.",

    "And when you learn that, you stop fighting life so blindly. You listen better. You move with more precision. And your choices begin to carry less panic, and more trust.",

    "If this episode opened something for you, stay with me. This is only the first layer.",
]

print("Loading Chatterbox Turbo...")
model = ChatterboxTTS.from_pretrained(device="mps")

# Add 0.5s silence between paragraphs
silence = torch.zeros(1, int(0.5 * model.sr))

chunks = []
total_dur = 0.0
start_all = time.time()

for i, para in enumerate(PARAGRAPHS):
    t0 = time.time()
    wav = model.generate(para, audio_prompt_path=REF_AUDIO, exaggeration=EXAGGERATION, cfg_weight=0.5)
    dur = wav.shape[-1] / model.sr
    chunks.append(wav)
    # Add silence between paragraphs (not after last)
    if i < len(PARAGRAPHS) - 1:
        chunks.append(silence)
    total_dur += dur
    elapsed = time.time() - t0
    print(f"[{i+1:02d}/{len(PARAGRAPHS)}] {dur:.1f}s (gen: {elapsed:.0f}s) | {para[:60]}...")

# Concatenate
print("\nConcatenating...")
full_wav = torch.cat(chunks, dim=-1)
total_dur = full_wav.shape[-1] / model.sr

filename = "ep01_full_chatterbox.wav"
filepath = f"{OUTPUT_DIR}/{filename}"
ta.save(filepath, full_wav, model.sr)

total_time = time.time() - start_all
print(f"\nDone: {filename}")
print(f"Duration: {total_dur:.1f}s ({total_dur/60:.1f}min)")
print(f"Total gen time: {total_time:.0f}s ({total_time/60:.1f}min)")
print(f"Chunks: {len(PARAGRAPHS)}")
