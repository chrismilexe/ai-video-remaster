$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$ConfigPath = Join-Path $RepoRoot "config\library.json"
$ExampleConfigPath = Join-Path $RepoRoot "config\library.example.json"

if (-not (Test-Path $ConfigPath)) {
    Write-Host "Missing config\library.json. Copy config\library.example.json and edit it first." -ForegroundColor Yellow
    Write-Host "Example: Copy-Item $ExampleConfigPath $ConfigPath" -ForegroundColor Yellow
    exit 1
}

$Config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
$CondaBat = "$env:USERPROFILE\miniconda3\condabin\conda.bat"

if (-not (Test-Path $CondaBat)) {
    Write-Host "Conda not found: $CondaBat" -ForegroundColor Red
    exit 1
}

$LibraryRoot = $Config.library_root
if (-not $LibraryRoot) {
    Write-Host "library_root is missing in config\library.json" -ForegroundColor Red
    exit 1
}

$IncomingDir = Join-Path $LibraryRoot "incoming"
$AssetsDir = Join-Path $LibraryRoot "assets"
$ManifestDir = Join-Path $LibraryRoot "manifests"
New-Item -ItemType Directory -Force -Path $LibraryRoot, $IncomingDir, $AssetsDir, $ManifestDir | Out-Null

$EnvName = $Config.whisperx_env
if (-not $EnvName) {
    $EnvName = "whisperx"
}

Write-Host "========================================" -ForegroundColor Magenta
Write-Host "  Video2Audio Batch Ingest" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta
Write-Host "Conda env    : $EnvName" -ForegroundColor Cyan
Write-Host "Library root : $LibraryRoot" -ForegroundColor Cyan
Write-Host "Incoming dir : $IncomingDir" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Magenta

$PythonArgs = @(
    "run",
    "-n",
    $EnvName,
    "python",
    (Join-Path $RepoRoot "scripts\batch_ingest.py"),
    "--config",
    $ConfigPath
)

if ($args.Count -gt 0) {
    $PythonArgs += $args
}

& $CondaBat @PythonArgs
exit $LASTEXITCODE
