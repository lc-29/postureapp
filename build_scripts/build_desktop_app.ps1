param(
    [string]$ProjectRoot = (Resolve-Path "$PSScriptRoot\..").Path
)

$ErrorActionPreference = "Stop"
Set-Location $ProjectRoot

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    throw "Khong tim thay .venv. Hay tao venv va cai requirements truoc."
}

.\.venv\Scripts\python.exe -m pip install pyinstaller
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe -m py_compile `
    src/4_main_desktop_app.py `
    src/3_database_setup.py `
    src/runtime_paths.py `
    src/posture_baseline.py `
    src/statistics_service.py `
    src/utils.py

.\.venv\Scripts\pyinstaller.exe --clean --noconfirm build_scripts/posture_app.spec

Write-Host "Build done: dist\PostureDetectionApp\PostureDetectionApp.exe"
