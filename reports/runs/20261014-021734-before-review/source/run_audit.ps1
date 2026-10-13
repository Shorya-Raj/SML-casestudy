$ErrorActionPreference = "Stop"

# Resolve the repository root from this script so it runs from any current
# directory, then ask the Python audit script for a serialized output bundle.
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$reportDirectory = Join-Path $projectRoot "reports"
New-Item -ItemType Directory -Force -Path $reportDirectory | Out-Null
$bundleOutput = python .\scripts\audit_unsw_nb15.py --emit-bundle | Out-String
if ($LASTEXITCODE -ne 0) {
    throw "The UNSW-NB15 audit process failed with exit code $LASTEXITCODE."
}

# The desktop's restricted Python process cannot create files in the OneDrive
# workspace. PowerShell writes the derived reports without modifying data/raw.
$bundle = $bundleOutput | ConvertFrom-Json
$utf8WithoutBom = [System.Text.UTF8Encoding]::new($false)
[System.IO.File]::WriteAllText(
    (Join-Path $projectRoot "reports\unsw_nb15_audit.json"),
    [string]$bundle.json_text,
    $utf8WithoutBom
)
[System.IO.File]::WriteAllText(
    (Join-Path $projectRoot "reports\unsw_nb15_data_audit.md"),
    [string]$bundle.markdown_text,
    $utf8WithoutBom
)

Write-Output "Wrote reports\unsw_nb15_audit.json"
Write-Output "Wrote reports\unsw_nb15_data_audit.md"
