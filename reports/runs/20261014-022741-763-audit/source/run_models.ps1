param([string]$Python = '')
# Use the shared runner so audits and models have the same environment,
# dated output snapshots, and success/failure logging.
& (Join-Path $PSScriptRoot 'run_project.ps1') -Task 'models' -Python $Python
