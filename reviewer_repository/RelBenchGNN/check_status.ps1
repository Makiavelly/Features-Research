$taskRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
foreach ($seed in 42, 43, 44, 45, 46) {
    $outputDir = Join-Path $taskRoot "results\seed_$seed"
    $metricsPath = Join-Path $outputDir 'metrics.json'
    $historyPath = Join-Path $outputDir 'history.json'
    if (Test-Path -LiteralPath $metricsPath) {
        $metrics = Get-Content -LiteralPath $metricsPath -Raw | ConvertFrom-Json
        [PSCustomObject]@{ Seed=$seed; Status='complete'; Epoch=20; ValMAPPercent=100*$metrics.val_metrics.map; TestMAPPercent=100*$metrics.test_metrics.map }
    } elseif (Test-Path -LiteralPath $historyPath) {
        $history = @(Get-Content -LiteralPath $historyPath -Raw | ConvertFrom-Json)
        $last = $history[-1]
        [PSCustomObject]@{ Seed=$seed; Status='incomplete (inspect log/process)'; Epoch=$last.epoch; ValMAPPercent=100*$last.val_metrics.map; TestMAPPercent=$null }
    } else {
        [PSCustomObject]@{ Seed=$seed; Status='no completed epoch'; Epoch=0; ValMAPPercent=$null; TestMAPPercent=$null }
    }
}
