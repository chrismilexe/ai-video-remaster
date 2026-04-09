import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "batch_ingest.py"
SPEC = importlib.util.spec_from_file_location("batch_ingest", MODULE_PATH)
batch_ingest = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(batch_ingest)


class BatchIngestTests(unittest.TestCase):
    def test_build_asset_id_uses_slugified_stem_and_sha_prefix(self):
        asset_id = batch_ingest.build_asset_id("Timing Judgement EP01.mp4", "abcdef1234567890")
        self.assertEqual(asset_id, "timing_judgement_ep01_abcdef12")

    def test_scan_media_files_recurses_and_filters_by_extension(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "nested").mkdir()
            keep_a = root / "lesson01.mp4"
            keep_b = root / "nested" / "lesson02.wav"
            skip = root / "notes.txt"
            keep_a.write_bytes(b"a")
            keep_b.write_bytes(b"b")
            skip.write_text("skip", encoding="utf-8")

            files = batch_ingest.scan_media_files(
                [str(root)],
                video_extensions=[".mp4", ".mkv"],
                audio_extensions=[".wav", ".mp3"],
            )

            self.assertEqual(files, [keep_a.resolve(), keep_b.resolve()])

    def test_render_raw_markdown_includes_metadata_and_segment_text(self):
        metadata = {
            "asset_id": "sample_12345678",
            "source_name": "sample.mp4",
            "source_path": "D:/incoming/sample.mp4",
            "sha256": "1234567890abcdef",
            "language": "zh",
            "model": "large-v3",
            "diarized": False,
        }
        transcript = {
            "language": "zh",
            "segments": [
                {"start": 0.0, "end": 1.2, "text": "第一句。"},
                {"start": 1.2, "end": 2.8, "text": "第二句。"},
            ],
        }

        markdown = batch_ingest.render_raw_markdown(metadata, transcript)

        self.assertIn("# 中文原始文稿", markdown)
        self.assertIn("sample_12345678", markdown)
        self.assertIn("D:/incoming/sample.mp4", markdown)
        self.assertIn("第一句。", markdown)
        self.assertIn("第二句。", markdown)

    def test_upsert_manifest_replaces_existing_entry_for_same_sha(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = Path(tmpdir) / "library_index.jsonl"
            original = {
                "asset_id": "old_asset",
                "sha256": "samehash",
                "status": "done",
            }
            manifest_path.write_text(json.dumps(original, ensure_ascii=False) + "\n", encoding="utf-8")

            updated = {
                "asset_id": "new_asset",
                "sha256": "samehash",
                "status": "done",
                "model": "large-v3",
            }
            other = {
                "asset_id": "other_asset",
                "sha256": "otherhash",
                "status": "done",
            }

            batch_ingest.upsert_manifest_entry(manifest_path, updated)
            batch_ingest.upsert_manifest_entry(manifest_path, other)

            rows = [
                json.loads(line)
                for line in manifest_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]

            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["asset_id"], "new_asset")
            self.assertEqual(rows[1]["asset_id"], "other_asset")

    def test_ingest_file_creates_canonical_outputs_and_manifest_entry(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "incoming" / "lesson01.mp4"
            source.parent.mkdir(parents=True)
            source.write_bytes(b"video-bytes")

            paths = batch_ingest.ensure_library_structure(root / "library")
            config = dict(batch_ingest.DEFAULT_CONFIG)
            config["library_root"] = str(paths["root"])
            config["input_dirs"] = [str(source.parent)]

            def fake_run_whisperx(command):
                output_dir = Path(command[command.index("--output_dir") + 1])
                output_dir.mkdir(parents=True, exist_ok=True)
                (output_dir / "lesson01.json").write_text(
                    json.dumps(
                        {
                            "language": "zh",
                            "segments": [
                                {"start": 0.0, "end": 1.0, "text": "第一段"},
                                {"start": 1.0, "end": 2.0, "text": "第二段"},
                            ],
                        },
                        ensure_ascii=False,
                    ),
                    encoding="utf-8",
                )
                (output_dir / "lesson01.srt").write_text(
                    "1\n00:00:00,000 --> 00:00:01,000\n第一段\n",
                    encoding="utf-8",
                )

            with mock.patch.object(batch_ingest, "run_whisperx", side_effect=fake_run_whisperx):
                entry = batch_ingest.ingest_file(source, config, paths)

            asset_dir = paths["assets"] / entry["asset_id"]
            self.assertTrue((asset_dir / "transcript.json").exists())
            self.assertTrue((asset_dir / "transcript.srt").exists())
            self.assertTrue((asset_dir / "raw_zh.md").exists())
            self.assertTrue((asset_dir / "metadata.json").exists())

            rows = batch_ingest.load_manifest_entries(paths["manifest"])
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["asset_id"], entry["asset_id"])
            self.assertEqual(rows[0]["status"], "done")

    def test_ingest_file_skips_when_same_sha_already_exists(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "incoming" / "lesson01.mp4"
            source.parent.mkdir(parents=True)
            source.write_bytes(b"video-bytes")

            paths = batch_ingest.ensure_library_structure(root / "library")
            sha256 = batch_ingest.compute_sha256(source)
            batch_ingest.upsert_manifest_entry(
                paths["manifest"],
                {
                    "asset_id": "lesson01_existing",
                    "sha256": sha256,
                    "source_path": str(source.resolve()),
                    "source_name": source.name,
                    "status": "done",
                    "model": "large-v3",
                    "language": "zh",
                    "diarized": False,
                    "duration_seconds": 2.0,
                    "transcript_srt_path": "srt",
                    "transcript_json_path": "json",
                    "raw_text_path": "raw",
                    "ingested_at": "2026-04-09T00:00:00Z",
                },
            )

            config = dict(batch_ingest.DEFAULT_CONFIG)

            with mock.patch.object(batch_ingest, "run_whisperx") as mocked_run:
                result = batch_ingest.ingest_file(source, config, paths)

            self.assertEqual(result["status"], "skipped")
            self.assertEqual(result["reason"], "sha256_exists")
            mocked_run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
