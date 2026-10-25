$workspace = Split-Path -Parent $PSScriptRoot
$taskOut = Join-Path $PSScriptRoot 'results/qwen25coder7b_seed42_v2'
New-Item -ItemType Directory -Force -Path $taskOut | Out-Null
$pidPath = Join-Path $taskOut 'windows_launcher.pid'
if (Test-Path -LiteralPath $pidPath) {
    $existing = Get-Process -Id ([int](Get-Content -LiteralPath $pidPath)) -ErrorAction SilentlyContinue
    if ($existing -and $existing.ProcessName -eq 'wsl') { Write-Output 'LLM-FE pipeline already active'; exit 0 }
}
$process = Start-Process -FilePath 'wsl.exe' -ArgumentList @('-d','Ubuntu','--','bash','LLMFeatures/pipeline.sh') -WorkingDirectory $workspace -WindowStyle Hidden -RedirectStandardOutput (Join-Path $taskOut 'pipeline.log') -RedirectStandardError (Join-Path $taskOut 'pipeline.stderr.log') -PassThru
$process.Id | Set-Content -LiteralPath $pidPath
Write-Output "Started LLM-FE pipeline: $($process.Id)"
