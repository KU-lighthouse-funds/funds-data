# Regenerate site JSON from v4.csv and show what to commit next.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "Syncing programmes.json from v4.csv..." -ForegroundColor Cyan
python funds-overview-site/sync_data.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "  1. Commit here (data repo):  funds with KU support - v4.csv + any script changes"
Write-Host "  2. Commit site repo:         cd funds-overview-site; git add data/programmes.json; git commit; git push"
Write-Host "     Live site: https://ku-lighthouse-funds.github.io/funds-overview/"
