#!/usr/bin/env python3
"""Batch ingest media into a transcript-first content library."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional


DEFAULT_CONFIG = {
    "library_root": r"D:\Video2AudioLibrary",
    "input_dirs": [r"D:\Video2AudioLibrary\incoming"],
    "whisperx_env": "whisperx",
    "default_model": "large-v3",
    "default_language": "zh",
    "batch_size": 16,
    "compute_type": "float16",
    "enable_diarization": False,
    "device": "cuda",
    "video_extensions": [
        ".mp4",
        ".mkv",
        ".mov",
        ".avi",
        ".wmv",
        ".m4v",
        ".flv",
        ".webm",
    ],
    "audio_extensions": [
        ".mp3",
        ".wav",
        ".m4a",
        ".aac",
        ".flac",
        ".ogg",
        ".wma",
    ],
    "hf_token": "",
}


class IngestError(RuntimeError):
    """Raised when ingest cannot complete."""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify_filename(name: str) -> str:
    stem = Path(name).stem.lower()
    stem = re.sub(r"[^\w]+", "_", stem, flags=re.UNICODE)
    stem = re.sub(r"_+", "_", stem).strip("_")
    return stem or "asset"


def build_asset_id(source_name: str, sha256: str) -> str:
    return f"{slugify_filename(source_name)}_{sha256[:8]}"


def compute_sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def scan_media_files(
    input_dirs: Iterable[str],
    video_extensions: Iterable[str],
    audio_extensions: Iterable[str],
) -> List[Path]:
    allowed = {ext.lower() for ext in video_extensions}
    allowed.update(ext.lower() for ext in audio_extensions)
    results: List[Path] = []

    for directory in input_dirs:
        root = Path(directory).expanduser()
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in allowed:
                results.append(path.resolve())

    results.sort()
    return results


def render_raw_markdown(metadata: Dict[str, object], transcript: Dict[str, object]) -> str:
    lines = [
        "# 中文原始文稿",
        "",
        "## 元数据",
        "",
        f"- asset_id: {metadata.get('asset_id', '')}",
        f"- source_name: {metadata.get('source_name', '')}",
        f"- source_path: {metadata.get('source_path', '')}",
        f"- sha256: {metadata.get('sha256', '')}",
        f"- language: {metadata.get('language', '')}",
        f"- model: {metadata.get('model', '')}",
        f"- diarized: {metadata.get('diarized', '')}",
        f"- ingested_at: {metadata.get('ingested_at', '')}",
        "",
        "## 文稿",
        "",
    ]

    for segment in transcript.get("segments", []):
        text = str(segment.get("text", "")).strip()
        if text:
            lines.append(text)
            lines.append("")

    return "\n".join(lines).strip() + "\n"


def load_manifest_entries(manifest_path: Path) -> List[Dict[str, object]]:
    if not manifest_path.exists():
        return []

    rows: List[Dict[str, object]] = []
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def upsert_manifest_entry(manifest_path: Path, entry: Dict[str, object]) -> None:
    rows = load_manifest_entries(manifest_path)
    replaced = False

    for index, row in enumerate(rows):
        if row.get("sha256") == entry.get("sha256"):
            rows[index] = entry
            replaced = True
            break

    if not replaced:
        rows.append(entry)

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    payload = "\n".join(json.dumps(row, ensure_ascii=False) for row in rows)
    manifest_path.write_text(payload + ("\n" if payload else ""), encoding="utf-8")


def load_config(config_path: Path) -> Dict[str, object]:
    config = dict(DEFAULT_CONFIG)
    if config_path.exists():
        user_config = json.loads(config_path.read_text(encoding="utf-8"))
        config.update(user_config)
    return config


def ensure_library_structure(library_root: Path) -> Dict[str, Path]:
    library_root = library_root.expanduser().resolve()
    paths = {
        "root": library_root,
        "incoming": library_root / "incoming",
        "assets": library_root / "assets",
        "manifests": library_root / "manifests",
        "manifest": library_root / "manifests" / "library_index.jsonl",
    }
    for path in [paths["root"], paths["incoming"], paths["assets"], paths["manifests"]]:
        path.mkdir(parents=True, exist_ok=True)
    return paths


def extract_duration_seconds(transcript: Dict[str, object]) -> Optional[float]:
    segments = transcript.get("segments") or []
    if not segments:
        return None
    try:
        return float(segments[-1].get("end"))
    except (TypeError, ValueError, AttributeError):
        return None


def build_whisperx_command(
    source_path: Path,
    output_dir: Path,
    model: str,
    language: str,
    device: str,
    compute_type: str,
    batch_size: int,
    diarize: bool,
    hf_token: str,
) -> List[str]:
    whisperx_executable = resolve_whisperx_executable()
    command = [
        whisperx_executable,
        str(source_path),
        "--model",
        model,
        "--language",
        language,
        "--device",
        device,
        "--compute_type",
        compute_type,
        "--batch_size",
        str(batch_size),
        "--output_dir",
        str(output_dir),
        "--output_format",
        "all",
    ]
    if diarize:
        command.append("--diarize")
        if hf_token:
            command.extend(["--hf_token", hf_token])
    return command


def resolve_whisperx_executable() -> str:
    env_python = Path(sys.executable).resolve()
    candidates = []

    if os.name == "nt":
        candidates.extend(
            [
                env_python.parent / "Scripts" / "whisperx.exe",
                env_python.parent / "Scripts" / "whisperx",
                env_python.parent / "whisperx.exe",
            ]
        )
    else:
        candidates.extend(
            [
                env_python.parent / "whisperx",
                env_python.parent.parent / "bin" / "whisperx",
            ]
        )

    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    resolved = shutil.which("whisperx")
    if resolved:
        return resolved

    raise IngestError("Could not locate whisperx executable for the current Python environment.")


def run_whisperx(
    command: List[str],
    cwd: Optional[Path] = None,
) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=str(cwd) if cwd else None, check=True)


def normalize_whisperx_output(temp_output_dir: Path, asset_dir: Path) -> Dict[str, Path]:
    json_candidates = sorted(temp_output_dir.glob("*.json"))
    srt_candidates = sorted(temp_output_dir.glob("*.srt"))

    if not json_candidates:
        raise IngestError("WhisperX did not produce a .json transcript file.")
    if not srt_candidates:
        raise IngestError("WhisperX did not produce a .srt transcript file.")

    target_json = asset_dir / "transcript.json"
    target_srt = asset_dir / "transcript.srt"

    shutil.copy2(json_candidates[0], target_json)
    shutil.copy2(srt_candidates[0], target_srt)

    return {
        "json": target_json,
        "srt": target_srt,
    }


def create_metadata(
    asset_id: str,
    source_path: Path,
    sha256: str,
    model: str,
    language: str,
    diarized: bool,
    duration_seconds: Optional[float],
    status: str,
) -> Dict[str, object]:
    return {
        "asset_id": asset_id,
        "sha256": sha256,
        "source_path": str(source_path.resolve()),
        "source_name": source_path.name,
        "model": model,
        "language": language,
        "diarized": diarized,
        "duration_seconds": duration_seconds,
        "status": status,
        "ingested_at": utc_now_iso(),
    }


def write_json(path: Path, payload: Dict[str, object]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def manifest_entry_from_metadata(
    metadata: Dict[str, object],
    transcript_srt_path: Path,
    transcript_json_path: Path,
    raw_text_path: Path,
) -> Dict[str, object]:
    return {
        "asset_id": metadata["asset_id"],
        "sha256": metadata["sha256"],
        "source_path": metadata["source_path"],
        "source_name": metadata["source_name"],
        "status": metadata["status"],
        "model": metadata["model"],
        "language": metadata["language"],
        "diarized": metadata["diarized"],
        "duration_seconds": metadata["duration_seconds"],
        "transcript_srt_path": str(transcript_srt_path.resolve()),
        "transcript_json_path": str(transcript_json_path.resolve()),
        "raw_text_path": str(raw_text_path.resolve()),
        "ingested_at": metadata["ingested_at"],
    }


def ingest_file(
    source_path: Path,
    config: Dict[str, object],
    paths: Dict[str, Path],
    force: bool = False,
    fast: bool = False,
    diarize: Optional[bool] = None,
) -> Dict[str, object]:
    sha256 = compute_sha256(source_path)
    manifest_rows = load_manifest_entries(paths["manifest"])
    existing = next((row for row in manifest_rows if row.get("sha256") == sha256), None)

    if existing and not force:
        return {
            "status": "skipped",
            "reason": "sha256_exists",
            "asset_id": existing["asset_id"],
            "source_path": str(source_path.resolve()),
            "sha256": sha256,
        }

    asset_id = build_asset_id(source_path.name, sha256)
    asset_dir = paths["assets"] / asset_id
    asset_dir.mkdir(parents=True, exist_ok=True)

    use_diarize = config["enable_diarization"] if diarize is None else diarize
    use_diarize = bool(use_diarize)
    hf_token = str(config.get("hf_token", "") or "")
    if use_diarize and not hf_token:
        raise IngestError("Diarization requested but hf_token is missing in config.")

    model = "large-v3-turbo" if fast else str(config["default_model"])
    language = str(config["default_language"])
    temp_output_dir = asset_dir / "_whisperx"
    if temp_output_dir.exists():
        shutil.rmtree(temp_output_dir)
    temp_output_dir.mkdir(parents=True, exist_ok=True)

    command = build_whisperx_command(
        source_path=source_path,
        output_dir=temp_output_dir,
        model=model,
        language=language,
        device=str(config["device"]),
        compute_type=str(config["compute_type"]),
        batch_size=int(config["batch_size"]),
        diarize=use_diarize,
        hf_token=hf_token,
    )

    run_whisperx(command)
    normalized = normalize_whisperx_output(temp_output_dir, asset_dir)
    transcript = json.loads(normalized["json"].read_text(encoding="utf-8"))
    duration_seconds = extract_duration_seconds(transcript)

    metadata = create_metadata(
        asset_id=asset_id,
        source_path=source_path,
        sha256=sha256,
        model=model,
        language=language,
        diarized=use_diarize,
        duration_seconds=duration_seconds,
        status="done",
    )
    raw_text_path = asset_dir / "raw_zh.md"
    metadata_path = asset_dir / "metadata.json"
    raw_text_path.write_text(render_raw_markdown(metadata, transcript), encoding="utf-8")
    write_json(metadata_path, metadata)

    entry = manifest_entry_from_metadata(
        metadata=metadata,
        transcript_srt_path=normalized["srt"],
        transcript_json_path=normalized["json"],
        raw_text_path=raw_text_path,
    )
    upsert_manifest_entry(paths["manifest"], entry)

    shutil.rmtree(temp_output_dir, ignore_errors=True)
    return entry


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Batch ingest media into transcript library")
    parser.add_argument("--config", default="config/library.json", help="Path to library config JSON")
    parser.add_argument("--fast", action="store_true", help="Use large-v3-turbo for faster ingest")
    parser.add_argument("--diarize", action="store_true", help="Enable speaker diarization")
    parser.add_argument("--force", action="store_true", help="Re-run ingest even if sha256 already exists")
    parser.add_argument("--limit", type=int, default=0, help="Only process the first N files")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    config_path = Path(args.config)
    config = load_config(config_path)
    library_root = Path(str(config["library_root"])).expanduser()
    paths = ensure_library_structure(library_root)
    files = scan_media_files(
        input_dirs=config["input_dirs"],
        video_extensions=config["video_extensions"],
        audio_extensions=config["audio_extensions"],
    )

    if args.limit and args.limit > 0:
        files = files[: args.limit]

    print(f"[batch-ingest] library_root={paths['root']}")
    print(f"[batch-ingest] discovered_files={len(files)}")

    processed = 0
    skipped = 0
    failed = 0

    for source_path in files:
        try:
            result = ingest_file(
                source_path=source_path,
                config=config,
                paths=paths,
                force=args.force,
                fast=args.fast,
                diarize=args.diarize,
            )
            if result.get("status") == "skipped":
                skipped += 1
                print(f"[skip] {source_path}")
            else:
                processed += 1
                print(f"[done] {source_path} -> {result['asset_id']}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"[fail] {source_path}: {exc}", file=sys.stderr)

    print(
        "[summary] "
        f"processed={processed} skipped={skipped} failed={failed} manifest={paths['manifest']}"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
