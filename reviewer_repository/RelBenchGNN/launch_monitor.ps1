$taskRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$workspace = Split-Path -Parent $taskRoot
$logs = Join-Path $taskRoot 'logs'
$pidPath = Join-Path $logs 'monitor_windows.pid'
if (Test-Path -LiteralPath $pidPath) {
    $monitorId = [int](Get-Content -LiteralPath $pidPath)
    $existing = Get-Process -Id $monitorId -ErrorAction SilentlyContinue
    if ($existing -and $existing.ProcessName -eq 'wsl') {
        Write-Output "Monitor already running: $monitorId"
        exit 0
    }
}
$process = Start-Process -FilePath 'wsl.exe' -ArgumentList @('-d','Ubuntu','--','RelBenchGNN/.venv-wsl/bin/python','-u','RelBenchGNN/monitor.py') -WorkingDirectory $workspace -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logs 'monitor.log') -RedirectStandardError (Join-Path $logs 'monitor.stderr.log') -PassThru
$process.Id | Set-Content -LiteralPath $pidPath
Write-Output "Started history monitor: $($process.Id)"
