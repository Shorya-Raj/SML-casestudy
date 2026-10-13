param(
    [ValidateSet('audit', 'models')][string]$Task = 'models',
    [string]$Python = ''
)
$ErrorActionPreference = 'Stop'

# One environment is used for both tasks. Install requirements once using the
# README; the runner does not install packages or change global Python.
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
if (-not $Python) {
    $localPython = Join-Path $projectRoot '.venv/Scripts/python.exe'
    $Python = if (Test-Path -LiteralPath $localPython) { $localPython } else { 'python' }
}
$utf8 = [Text.UTF8Encoding]::new($false)
$start = [DateTimeOffset]::UtcNow.ToOffset([TimeSpan]::FromHours(5.5))
$runId = $start.ToString('yyyyMMdd-HHmmss-fff') + '-' + $Task
$reports = Join-Path $projectRoot 'reports'
$runDirectory = Join-Path $reports ('runs/' + $runId)
New-Item -ItemType Directory -Path (Join-Path $runDirectory 'source') -Force | Out-Null
$status = 'running'
$failure = ''
$outputs = @()
$runtime = $null
$notes = [Collections.Generic.List[string]]::new()
$notes.Add('Task: ' + $Task + '; started IST: ' + $start.ToString('o'))
$notes.Add('Python command: ' + $Python)

# Save the exact code and dependency pins before execution. Failed runs keep
# this folder too, so their evidence can be inspected without changing inputs.
function Invoke-ProjectPython([string]$Script, [string[]]$Arguments) {
    $textOutput = & $Python (Join-Path $PSScriptRoot $Script) @Arguments 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) {
        [IO.File]::WriteAllText((Join-Path $runDirectory 'python_error.log'), $textOutput, $utf8)
        throw ('Python step failed: ' + $Script + '. See this run folder for the error.')
    }
    return $textOutput
}

try {
    Get-ChildItem -LiteralPath $PSScriptRoot -File | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $runDirectory 'source')
    }
    Copy-Item -LiteralPath (Join-Path $projectRoot 'requirements.txt') -Destination (Join-Path $runDirectory 'source')

    if ($Task -eq 'audit') {
        $bundle = (Invoke-ProjectPython 'audit_unsw_nb15.py' @('--emit-bundle')) | ConvertFrom-Json
        $record = $bundle.json_text | ConvertFrom-Json
        $runtime = $record.runtime
        [IO.File]::WriteAllText((Join-Path $runDirectory 'unsw_nb15_audit.json'), [string]$bundle.json_text, $utf8)
        [IO.File]::WriteAllText((Join-Path $runDirectory 'unsw_nb15_data_audit.md'), [string]$bundle.markdown_text, $utf8)
        $checks = $record.integrity_and_scope_checks
        if (-not ($checks.all_sizes_match_expected -and $checks.all_hashes_match_expected -and $checks.all_row_counts_match_expected -and $checks.same_train_test_schema -and $checks.label_values_only_0_or_1)) {
            throw 'The audit found an input integrity/schema/label mismatch; inspect the archived audit.'
        }
        $outputs = @('unsw_nb15_audit.json', 'unsw_nb15_data_audit.md')
        foreach ($step in $record.processing_log) { $notes.Add([string]$step) }
        foreach ($split in $record.splits.PSObject.Properties) {
            $notes.Add(('Input {0}: {1} rows; {2} bytes; SHA-256 {3}' -f $split.Name, $split.Value.rows, $split.Value.actual_bytes, $split.Value.sha256))
        }
    } else {
        $bundle = (Invoke-ProjectPython 'train_unsw_nb15_models.py' @('--emit-bundle')) | ConvertFrom-Json
        $record = $bundle.json_text | ConvertFrom-Json
        $runtime = $record.metadata.runtime
        $resultPath = Join-Path $runDirectory 'unsw_nb15_model_results.json'
        [IO.File]::WriteAllText($resultPath, [string]$bundle.json_text, $utf8)
        [IO.File]::WriteAllText((Join-Path $runDirectory 'unsw_nb15_model_results.md'), [string]$bundle.markdown_text, $utf8)
        [IO.File]::WriteAllText((Join-Path $runDirectory 'unsw_nb15_model_metrics.csv'), [string]$bundle.csv_text, $utf8)
        $plots = (Invoke-ProjectPython 'plot_unsw_nb15_results.py' @('--results', $resultPath, '--emit-bundle')) | ConvertFrom-Json
        [IO.File]::WriteAllBytes((Join-Path $runDirectory 'unsw_nb15_model_comparison.png'), [Convert]::FromBase64String([string]$plots.metric_comparison_png_base64))
        [IO.File]::WriteAllBytes((Join-Path $runDirectory 'unsw_nb15_confusion_matrices.png'), [Convert]::FromBase64String([string]$plots.confusion_matrices_png_base64))
        $outputs = @('unsw_nb15_model_results.json', 'unsw_nb15_model_results.md', 'unsw_nb15_model_metrics.csv', 'unsw_nb15_model_comparison.png', 'unsw_nb15_confusion_matrices.png')
        foreach ($step in $record.metadata.processing_log) { $notes.Add([string]$step) }
        foreach ($split in $record.metadata.inputs.PSObject.Properties) {
            $notes.Add(('Input {0}: {1} rows; {2} bytes; SHA-256 {3}' -f $split.Name, $split.Value.rows, $split.Value.bytes, $split.Value.sha256))
        }
        foreach ($model in $record.models.PSObject.Properties) {
            $m = $model.Value.metrics.test_official
            $notes.Add(('{0}: official-test accuracy={1:F4}, macro-F1={2:F4}, attack recall={3:F4}; fixed settings={4}' -f $model.Name, $m.accuracy, $m.macro_f1, $m.attack_recall, ($model.Value.settings | ConvertTo-Json -Compress)))
        }
        $notes.Add('Validation group overlap: ' + $record.metadata.validation.group_overlap_count)
        $notes.Add('Full effective classifier parameters, preprocessing policy, fit warnings, timings, and runtime versions are in the archived JSON.')
    }

    # Publish the convenient latest copies only after every computation and
    # chart has succeeded. The dated originals remain available for review.
    foreach ($name in $outputs) {
        Copy-Item -LiteralPath (Join-Path $runDirectory $name) -Destination (Join-Path $reports $name) -Force
    }
    $status = 'success'
} catch {
    $status = 'failed'
    $failure = $_.Exception.Message
    $notes.Add('Failure: ' + $failure)
} finally {
    $finish = [DateTimeOffset]::UtcNow.ToOffset([TimeSpan]::FromHours(5.5))
    $notes.Add('Finished IST: ' + $finish.ToString('o') + '; status: ' + $status)
    [IO.File]::WriteAllText((Join-Path $runDirectory 'execution_notes.log'), ($notes -join [Environment]::NewLine), $utf8)
    $manifest = [ordered]@{
        task = $Task; status = $status; started_ist = $start.ToString('o'); finished_ist = $finish.ToString('o')
        python_command = $Python; runtime = $runtime; failure = $failure
        files = @(Get-ChildItem -LiteralPath $runDirectory -File -Recurse | ForEach-Object {
            [ordered]@{path = $_.FullName.Substring($runDirectory.Length + 1); sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash}
        })
    }
    [IO.File]::WriteAllText((Join-Path $runDirectory 'run_manifest.json'), ($manifest | ConvertTo-Json -Depth 12), $utf8)
    $entry = @('', ('### ' + $finish.ToString('yyyy-MM-dd HH:mm:ss') + ' IST — ' + $Task + ' run: ' + $status), '', ('- Dated evidence: reports/runs/' + $runId + '/'))
    $entry += @($notes | ForEach-Object { '- ' + $_ })
    [IO.File]::AppendAllText((Join-Path $projectRoot 'ACTION_LOG.md'), (($entry -join [Environment]::NewLine) + [Environment]::NewLine), $utf8)
}
if ($status -ne 'success') { throw $failure }
Write-Output ('Completed ' + $Task + '. Latest copies: reports/; dated evidence: reports/runs/' + $runId)
