param(
    [string]$ProjectRoot = (Resolve-Path "$PSScriptRoot\..").Path,
    [switch]$Launch
)

$ErrorActionPreference = "Stop"
Set-Location $ProjectRoot

$DistDir = Join-Path $ProjectRoot "dist\PostureDetectionApp"
$ExePath = Join-Path $DistDir "PostureDetectionApp.exe"
$RequiredFiles = @(
    $ExePath,
    (Join-Path $DistDir "_internal\models\ann_best.keras"),
    (Join-Path $DistDir "_internal\models\scaler.pkl"),
    (Join-Path $DistDir "_internal\assets\sounds\alarm.wav")
)

foreach ($Path in $RequiredFiles) {
    if (-not (Test-Path $Path)) {
        throw "Thieu file runtime: $Path"
    }
}

$UserDb = Join-Path $env:LOCALAPPDATA "PostureDetectionApp\posture_app.db"
Write-Host "Runtime files OK."
Write-Host "Expected writable DB: $UserDb"

if ($Launch) {
    Start-Process -FilePath $ExePath -WorkingDirectory $DistDir
    Write-Host "Da mo app. Hay test manual: Start webcam/video, Stop, Light/Dark, Thong ke."
}
