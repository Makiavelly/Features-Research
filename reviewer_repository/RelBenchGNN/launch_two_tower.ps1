$taskRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$workspace = Split-Path -Parent $taskRoot
$destination = Join-Path $taskRoot 'results/two_tower_seed_42'
New-Item -ItemType Directory -Force -Path $destination | Out-Null
$pidPath = Join-Path $destination 'windows_launcher.pid'
if (Test-Path -LiteralPath $pidPath) {
    $existing = Get-Process -Id ([int](Get-Content -LiteralPath $pidPath)) -ErrorAction SilentlyContinue
    if ($existing -and $existing.ProcessName -eq 'wsl') { Write-Output 'Two-tower pipeline already active'; exit 0 }
}
$process = Start-Process -FilePath 'wsl.exe' -ArgumentList @('-d','Ubuntu','--','bash','RelBenchGNN/two_tower_pipeline.sh') -WorkingDirectory $workspace -WindowStyle Hidden -RedirectStandardOutput (Join-Path $destination 'pipeline.log') -RedirectStandardError (Join-Path $destination 'pipeline.stderr.log') -PassThru
$process.Id | Set-Content -LiteralPath $pidPath
Write-Output "Started two-tower pipeline: $($process.Id)"
