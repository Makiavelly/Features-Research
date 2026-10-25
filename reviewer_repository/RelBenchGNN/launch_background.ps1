param([switch]$Resume)
$taskRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$workspace = Split-Path -Parent $taskRoot
$logs = Join-Path $taskRoot 'logs'
$pidPath = Join-Path $logs 'windows_launcher.pid'
if (Test-Path -LiteralPath $pidPath) {
    $launcherId = [int](Get-Content -LiteralPath $pidPath)
    $existing = Get-Process -Id $launcherId -ErrorAction SilentlyContinue
    if ($existing -and $existing.ProcessName -eq 'wsl') {
        Write-Output "Pipeline launcher already running: $launcherId"
        & (Join-Path $taskRoot 'launch_monitor.ps1')
        exit 0
    }
}
$exitPath = Join-Path $logs 'pipeline.exitcode'
if (Test-Path -LiteralPath $exitPath) {
    Move-Item -LiteralPath $exitPath -Destination (Join-Path $logs ('pipeline.previous.' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.exitcode'))
}
$launchArguments = @('-d','Ubuntu','--','bash','RelBenchGNN/background_pipeline.sh')
if ($Resume) { $launchArguments += 'resume' }
$process = Start-Process -FilePath 'wsl.exe' -ArgumentList $launchArguments -WorkingDirectory $workspace -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logs 'pipeline.log') -RedirectStandardError (Join-Path $logs 'pipeline.stderr.log') -PassThru
$process.Id | Set-Content -LiteralPath $pidPath
Write-Output "Started pipeline launcher: $($process.Id)"
& (Join-Path $taskRoot 'launch_monitor.ps1')
