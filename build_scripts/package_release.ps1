param(
    [string]$ProjectRoot = (Resolve-Path "$PSScriptRoot\..").Path,
    [string]$Version = "0.1.0-demo"
)

$ErrorActionPreference = "Stop"
Set-Location $ProjectRoot

$DistDir = Join-Path $ProjectRoot "dist\PostureDetectionApp"
if (-not (Test-Path $DistDir)) {
    throw "Chua co dist\PostureDetectionApp. Hay build truoc."
}

$ReleaseRoot = Join-Path $ProjectRoot "release"
$ReleaseDir = Join-Path $ReleaseRoot "PostureDetectionApp_$Version"
$ZipPath = Join-Path $ReleaseRoot "PostureDetectionApp_$Version.zip"

if (Test-Path $ReleaseDir) {
    Remove-Item -LiteralPath $ReleaseDir -Recurse -Force
}
New-Item -ItemType Directory -Path $ReleaseDir -Force | Out-Null

Copy-Item -Path (Join-Path $DistDir "*") -Destination $ReleaseDir -Recurse -Force
Copy-Item -Path "release_docs\README_RUN_APP.md" -Destination (Join-Path $ReleaseDir "README_RUN_APP.md") -Force
Copy-Item -Path "release_docs\LICENSE_OR_NOTICE.md" -Destination (Join-Path $ReleaseDir "LICENSE_OR_NOTICE.md") -Force
Copy-Item -Path "release\VERSION.txt" -Destination (Join-Path $ReleaseDir "VERSION.txt") -Force

if (Test-Path $ZipPath) {
    Remove-Item -LiteralPath $ZipPath -Force
}
Compress-Archive -Path (Join-Path $ReleaseDir "*") -DestinationPath $ZipPath -Force

Write-Host "Release folder: $ReleaseDir"
Write-Host "Release zip: $ZipPath"
