# Synced Content Library

This directory stores a Git-synced snapshot of the processed content library.

Included:
- `assets/`: processed transcript assets for each source file
- `manifests/`: manifest and ingest logs

Excluded:
- `incoming/`: raw source media files are intentionally not tracked in Git

Other machines can use this snapshot for transcript review, topic clustering, and script development without re-running ingestion.
