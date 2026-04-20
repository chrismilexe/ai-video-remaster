#!/usr/bin/env python3
"""Prepare EP01 audio-generation inputs from the approved English master script."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EP01_MASTER = ROOT / "outputs" / "scripts" / "en" / "ep01_master.md"
REF_AUDIO = ROOT / "outputs" / "reference.wav"
REF_TEXT = ROOT / "outputs" / "ref_text.txt"
EN_REF_AUDIO = ROOT / "outputs" / "record_20260420.wav"
EN_REF_TEXT = ROOT / "outputs" / "ref_text_en_20260420.txt"
AUDIO_DIR = ROOT / "outputs" / "audio"
SAMPLE_TEXT_PATH = AUDIO_DIR / "ep01_sample_input.txt"
FULL_TEXT_PATH = AUDIO_DIR / "ep01_full_input.txt"
SAMPLE_TTS_TEXT_PATH = AUDIO_DIR / "ep01_sample_tts_input.txt"
FULL_TTS_TEXT_PATH = AUDIO_DIR / "ep01_full_tts_input.txt"
MANIFEST_PATH = AUDIO_DIR / "ep01_audio_manifest.json"

SAMPLE_MIN_WORDS = 180
SAMPLE_MAX_WORDS = 260


def repo_path(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def load_master_body(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    marker = "# 英文正文"
    if marker not in raw:
        raise RuntimeError(f"Could not find marker {marker!r} in {path}")
    body = raw.split(marker, 1)[1].strip()
    return normalize_text(body)


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def strip_stage_directions(text: str) -> str:
    lines = []
    for line in text.splitlines():
        cleaned = re.sub(r"\[(pause|beat)\]", "", line, flags=re.IGNORECASE).strip()
        cleaned = re.sub(r"\s{2,}", " ", cleaned)
        if cleaned:
            lines.append(cleaned)
    return "\n".join(lines).strip() + "\n"


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w']+\b", text))


def select_sample_text(full_text: str) -> str:
    paragraphs = [p.strip() for p in full_text.split("\n\n") if p.strip()]
    selected: list[str] = []
    running_words = 0

    for paragraph in paragraphs:
        paragraph_words = count_words(paragraph)
        if selected and running_words + paragraph_words > SAMPLE_MAX_WORDS:
            break
        selected.append(paragraph)
        running_words += paragraph_words
        if running_words >= SAMPLE_MIN_WORDS:
            break

    if not selected:
        raise RuntimeError("Failed to build EP01 sample text.")

    return "\n\n".join(selected).strip() + "\n"


def main() -> None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    full_text = load_master_body(EP01_MASTER)
    sample_text = select_sample_text(full_text)
    full_tts_text = strip_stage_directions(full_text)
    sample_tts_text = strip_stage_directions(sample_text)
    ref_text = REF_TEXT.read_text(encoding="utf-8").strip()
    preferred_ref_audio = EN_REF_AUDIO if EN_REF_AUDIO.exists() else None
    preferred_ref_text = EN_REF_TEXT if EN_REF_TEXT.exists() else None
    preferred_ref_text_preview = None

    if preferred_ref_text is not None:
        preferred_ref_text_preview = preferred_ref_text.read_text(encoding="utf-8").strip()[:120]

    SAMPLE_TEXT_PATH.write_text(sample_text, encoding="utf-8")
    FULL_TEXT_PATH.write_text(full_text, encoding="utf-8")
    SAMPLE_TTS_TEXT_PATH.write_text(sample_tts_text, encoding="utf-8")
    FULL_TTS_TEXT_PATH.write_text(full_tts_text, encoding="utf-8")

    manifest = {
        "episode_id": "ep01",
        "episode_title": "Why Smart People Keep Making Bad Timing Decisions",
        "default_reference_audio": repo_path(REF_AUDIO),
        "default_reference_text": repo_path(REF_TEXT),
        "default_reference_text_preview": ref_text[:120],
        "sample_input": repo_path(SAMPLE_TEXT_PATH),
        "sample_word_count": count_words(sample_text),
        "sample_tts_input": repo_path(SAMPLE_TTS_TEXT_PATH),
        "sample_tts_word_count": count_words(sample_tts_text),
        "full_input": repo_path(FULL_TEXT_PATH),
        "full_word_count": count_words(full_text),
        "full_tts_input": repo_path(FULL_TTS_TEXT_PATH),
        "full_tts_word_count": count_words(full_tts_text),
        "expected_sample_output": repo_path(AUDIO_DIR / "ep01_sample.wav"),
        "expected_preferred_sample_output": repo_path(AUDIO_DIR / "ep01_sample_en_ref.wav"),
        "expected_full_output": repo_path(AUDIO_DIR / "ep01_full.wav"),
    }
    if preferred_ref_audio is not None:
        manifest["preferred_local_reference_audio"] = repo_path(preferred_ref_audio)
    if preferred_ref_text is not None:
        manifest["preferred_local_reference_text"] = repo_path(preferred_ref_text)
    if preferred_ref_text_preview is not None:
        manifest["preferred_local_reference_text_preview"] = preferred_ref_text_preview
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote sample input: {SAMPLE_TEXT_PATH}")
    print(f"Wrote full input:   {FULL_TEXT_PATH}")
    print(f"Wrote sample TTS:   {SAMPLE_TTS_TEXT_PATH}")
    print(f"Wrote full TTS:     {FULL_TTS_TEXT_PATH}")
    print(f"Wrote manifest:     {MANIFEST_PATH}")
    print(f"Sample words:       {manifest['sample_word_count']}")
    print(f"Full words:         {manifest['full_word_count']}")


if __name__ == "__main__":
    main()
