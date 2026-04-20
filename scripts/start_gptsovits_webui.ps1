$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$GptSovitsRoot = "D:\AI-Tools\GPT-SoVITS"
$PythonExe = "$env:USERPROFILE\miniconda3\envs\gptsovits\python.exe"

if (-not (Test-Path $PythonExe)) {
    throw "Missing GPT-SoVITS python environment: $PythonExe"
}

if (-not (Test-Path $GptSovitsRoot)) {
    throw "Missing GPT-SoVITS checkout: $GptSovitsRoot"
}

Set-Location $GptSovitsRoot
& $PythonExe .\webui.py zh_CN
