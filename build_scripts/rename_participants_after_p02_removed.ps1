param(
    [string]$ProjectRoot = (Resolve-Path "$PSScriptRoot\..").Path,
    [switch]$Apply
)

$ErrorActionPreference = "Stop"
Set-Location $ProjectRoot

$videoRoots = @(
    "dataset\raw_videos\correct",
    "dataset\raw_videos\incorrect",
    "dataset\external_videos\correct",
    "dataset\external_videos\incorrect"
)

$participantMap = @{
    "P01" = "P01"
    "P03" = "P02"
    "P04" = "P03"
    "P05" = "P04"
    "P06" = "P05"
}

$extensions = @(".mp4", ".avi", ".mov", ".mkv", ".webm", ".m4v")
$rows = New-Object System.Collections.Generic.List[object]
$plannedMoves = New-Object System.Collections.Generic.List[object]

foreach ($root in $videoRoots) {
    $rootPath = Join-Path $ProjectRoot $root
    if (-not (Test-Path $rootPath)) {
        continue
    }

    Get-ChildItem -LiteralPath $rootPath -File | Where-Object {
        $extensions -contains $_.Extension.ToLowerInvariant()
    } | ForEach-Object {
        $file = $_
        $match = [regex]::Match($file.Name, "^(P\d+)_")
        $label = Split-Path -Leaf $file.DirectoryName
        $viewAngle = "unknown"
        if ($file.BaseName -match "_front_") {
            $viewAngle = "front"
        } elseif ($file.BaseName -match "_side_30_") {
            $viewAngle = "side_30"
        } elseif ($file.BaseName -match "_side_90_") {
            $viewAngle = "side_90"
        }

        if (-not $match.Success) {
            $rows.Add([pscustomobject]@{
                old_path = $file.FullName
                new_path = ""
                old_participant_id = ""
                new_participant_id = ""
                label = $label
                view_angle = $viewAngle
                status = "skip_unmatched"
            })
            return
        }

        $oldParticipant = $match.Groups[1].Value.ToUpperInvariant()
        if (-not $participantMap.ContainsKey($oldParticipant)) {
            $rows.Add([pscustomobject]@{
                old_path = $file.FullName
                new_path = ""
                old_participant_id = $oldParticipant
                new_participant_id = ""
                label = $label
                view_angle = $viewAngle
                status = "skip_unmapped"
            })
            return
        }

        $newParticipant = $participantMap[$oldParticipant]
        $newName = $file.Name -replace "^$oldParticipant`_", "$newParticipant`_"
        $newPath = Join-Path $file.DirectoryName $newName
        $status = if ($file.FullName -eq $newPath) { "unchanged" } else { "rename" }

        $row = [pscustomobject]@{
            old_path = $file.FullName
            new_path = $newPath
            old_participant_id = $oldParticipant
            new_participant_id = $newParticipant
            label = $label
            view_angle = $viewAngle
            status = $status
        }
        $rows.Add($row)
        if ($status -eq "rename") {
            $plannedMoves.Add($row)
        }
    }
}

$reportPath = Join-Path $ProjectRoot "reports\dataset_rename_plan.csv"
New-Item -ItemType Directory -Path (Split-Path $reportPath -Parent) -Force | Out-Null
$rows | Export-Csv -Path $reportPath -NoTypeInformation -Encoding UTF8

$duplicateTargets = $plannedMoves |
    Group-Object -Property new_path |
    Where-Object { $_.Count -gt 1 }
if ($duplicateTargets) {
    throw "Co target rename bi trung. Xem report: $reportPath"
}

$plannedOldPaths = @{}
foreach ($move in $plannedMoves) {
    $plannedOldPaths[$move.old_path] = $true
}

foreach ($move in $plannedMoves) {
    if ((Test-Path -LiteralPath $move.new_path) -and (-not $plannedOldPaths.ContainsKey($move.new_path))) {
        throw "File dich da ton tai va khong nam trong rename chain: $($move.new_path). Xem report: $reportPath"
    }
}

Write-Host "Rename plan written: $reportPath"
Write-Host "Total files scanned: $($rows.Count)"
Write-Host "Planned renames: $($plannedMoves.Count)"

if (-not $Apply) {
    Write-Host "Dry-run only. Re-run with -Apply to rename files."
    exit 0
}

foreach ($move in $plannedMoves) {
    $tempPath = "$($move.old_path).rename_tmp"
    if (Test-Path -LiteralPath $tempPath) {
        throw "File tam da ton tai: $tempPath"
    }
    Add-Member -InputObject $move -NotePropertyName temp_path -NotePropertyValue $tempPath
    Move-Item -LiteralPath $move.old_path -Destination $tempPath
}

foreach ($move in $plannedMoves) {
    Move-Item -LiteralPath $move.temp_path -Destination $move.new_path
}

Write-Host "Rename applied."
