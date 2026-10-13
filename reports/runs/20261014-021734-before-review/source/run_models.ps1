$ErrorActionPreference = "Stop"

# Resolve paths from this script so the run is independent of the user's
# current directory. Reports and the processing log stay in the project.
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$reportDirectory = Join-Path $projectRoot "reports"
New-Item -ItemType Directory -Force -Path $reportDirectory | Out-Null

# Prefer a reusable project environment. The temporary fallback supports the
# restricted Codex workspace, where Python cannot create files under OneDrive.
$projectPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$useSystemPip = $false
if (Test-Path -LiteralPath $projectPython) {
    $modelPython = $projectPython
} else {
    $tempEnvironment = Join-Path $env:TEMP "codex-sml-unsw-nb15-env"
    $modelPython = Join-Path $tempEnvironment "Scripts\python.exe"
    if (-not (Test-Path -LiteralPath $modelPython)) {
        python -m venv --without-pip $tempEnvironment
        if ($LASTEXITCODE -ne 0) {
            throw "Could not create a temporary isolated Python environment."
        }
    }
    $useSystemPip = $true
}

# Install only the pinned project requirements into the selected environment.
if ($useSystemPip) {
    python -m pip --python $modelPython install --disable-pip-version-check -r .\requirements.txt
} else {
    & $modelPython -m pip install --disable-pip-version-check -r .\requirements.txt
}
if ($LASTEXITCODE -ne 0) {
    throw "Package installation failed; no model run or test evaluation was performed."
}

# Python emits derived report text. PowerShell writes the files because direct
# Python file creation is blocked in this restricted OneDrive workspace.
$bundleOutput = & $modelPython .\scripts\train_unsw_nb15_models.py --emit-bundle | Out-String
$modelExitCode = $LASTEXITCODE
if ($modelExitCode -ne 0) {
    throw "The model workflow failed with exit code $modelExitCode; inspect the output before interpreting any results."
}
$bundle = $bundleOutput | ConvertFrom-Json
$utf8WithoutBom = [System.Text.UTF8Encoding]::new($false)
[System.IO.File]::WriteAllText((Join-Path $reportDirectory "unsw_nb15_model_results.json"), [string]$bundle.json_text, $utf8WithoutBom)
[System.IO.File]::WriteAllText((Join-Path $reportDirectory "unsw_nb15_model_results.md"), [string]$bundle.markdown_text, $utf8WithoutBom)
[System.IO.File]::WriteAllText((Join-Path $reportDirectory "unsw_nb15_model_metrics.csv"), [string]$bundle.csv_text, $utf8WithoutBom)

# Render charts from the saved metrics only, then write the PNG bytes here.
# This keeps plots reproducible without asking the plotting script to write
# directly into the restricted OneDrive workspace.
$plotOutput = & $modelPython .\scripts\plot_unsw_nb15_results.py --emit-bundle | Out-String
$plotExitCode = $LASTEXITCODE
if ($plotExitCode -ne 0) {
    throw "The metrics were saved, but figure generation failed with exit code $plotExitCode."
}
$plots = $plotOutput | ConvertFrom-Json
[System.IO.File]::WriteAllBytes((Join-Path $reportDirectory "unsw_nb15_model_comparison.png"), [Convert]::FromBase64String([string]$plots.metric_comparison_png_base64))
[System.IO.File]::WriteAllBytes((Join-Path $reportDirectory "unsw_nb15_confusion_matrices.png"), [Convert]::FromBase64String([string]$plots.confusion_matrices_png_base64))

# Add a concise run record with provenance, validation counts, and final metrics
# so future reruns append evidence instead of silently replacing history.
$run = $bundle.json_text | ConvertFrom-Json
$timestamp = $run.metadata.run_timestamp_local
$logLines = [System.Collections.Generic.List[string]]::new()
$logLines.Add("")
$logLines.Add("### $timestamp — Leakage-aware model comparison completed")
$logLines.Add("")
$logLines.Add(('- Runner: `scripts/run_models.ps1`; model code: `scripts/train_unsw_nb15_models.py`; environment versions: Python {0}, pandas {1}, NumPy {2}, scikit-learn {3}, Matplotlib {4}.' -f $run.metadata.runtime.python, $run.metadata.runtime.pandas, $run.metadata.runtime.numpy, $run.metadata.runtime.scikit_learn, $run.metadata.runtime.matplotlib))
$trainingInput = $run.metadata.inputs.training
$testingInput = $run.metadata.inputs.testing
$logLines.Add(('- Verified training input: {0} rows, {1} bytes, SHA-256 `{2}`. Testing input: {3} rows, {4} bytes, SHA-256 `{5}`. Raw files were not modified.' -f $trainingInput.rows, $trainingInput.bytes, $trainingInput.sha256, $testingInput.rows, $testingInput.bytes, $testingInput.sha256))
$logLines.Add(('- Target=`label` (attack=1). Predictors={0}; excluded: id and attack_cat. Seed={1}; validation={2}. Fit rows={3}, validation rows={4}, class counts fit={5}, validation={6}, group overlap={7}.' -f $run.metadata.feature_count, $run.metadata.seed, $run.metadata.validation.method, $run.metadata.validation.fit_rows, $run.metadata.validation.validation_rows, ($run.metadata.validation.fit_class_counts | ConvertTo-Json -Compress), ($run.metadata.validation.validation_class_counts | ConvertTo-Json -Compress), $run.metadata.validation.group_overlap_count))
$logLines.Add(('- Official test rows={0}; seen predictor rows={1}; unseen predictor rows={2}. Fixed settings and preprocessing steps are in `reports/unsw_nb15_model_results.json`.' -f $run.metadata.test_rows, $run.metadata.test_seen_predictor_rows, $run.metadata.test_unseen_predictor_rows))
foreach ($entry in $run.models.PSObject.Properties) {
    $testMetrics = $entry.Value.metrics.test_official
    $unseenMetrics = $entry.Value.metrics.test_unseen_predictor_vectors
    $fitNote = $run.metadata.fit_notes.PSObject.Properties[$entry.Name].Value
    $logLines.Add("- $($entry.Name): validation macro-F1=$('{0:F4}' -f $entry.Value.metrics.validation.macro_f1), attack recall=$('{0:F4}' -f $entry.Value.metrics.validation.attack_recall); official-test macro-F1=$('{0:F4}' -f $testMetrics.macro_f1), attack recall=$('{0:F4}' -f $testMetrics.attack_recall), accuracy=$('{0:F4}' -f $testMetrics.accuracy); unseen-vector macro-F1=$('{0:F4}' -f $unseenMetrics.macro_f1), attack recall=$('{0:F4}' -f $unseenMetrics.attack_recall); validation fit=$($fitNote.validation_fit_seconds)s, full-train fit=$($fitNote.full_training_fit_seconds)s.")
    foreach ($warning in @($fitNote.validation_warnings) + @($fitNote.final_fit_warnings)) {
        if ($warning) { $logLines.Add("  - Model warning: $warning") }
    }
}
$logLines.Add('- Outputs: `reports/unsw_nb15_model_results.md`, JSON companion, metrics CSV, metric-comparison PNG, and confusion-matrix PNG. See the Markdown report for class-wise metrics and caveats.')
[System.IO.File]::AppendAllText((Join-Path $projectRoot "ACTION_LOG.md"), (($logLines -join [Environment]::NewLine) + [Environment]::NewLine), $utf8WithoutBom)

Write-Output "Saved model results, metrics, and visualizations under reports\."
$summary = foreach ($entry in $run.models.PSObject.Properties) {
    [PSCustomObject]@{
        model = $entry.Name
        validation_macro_f1 = [math]::Round($entry.Value.metrics.validation.macro_f1, 4)
        test_macro_f1 = [math]::Round($entry.Value.metrics.test_official.macro_f1, 4)
        test_attack_recall = [math]::Round($entry.Value.metrics.test_official.attack_recall, 4)
        test_accuracy = [math]::Round($entry.Value.metrics.test_official.accuracy, 4)
        unseen_macro_f1 = [math]::Round($entry.Value.metrics.test_unseen_predictor_vectors.macro_f1, 4)
        unseen_attack_recall = [math]::Round($entry.Value.metrics.test_unseen_predictor_vectors.attack_recall, 4)
    }
}
$summary | Format-Table -AutoSize
