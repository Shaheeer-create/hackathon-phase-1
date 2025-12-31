# PowerShell script to run Todo CLI
# Run from PowerShell or double-click to execute

Write-Host "Running Todo CLI..." -ForegroundColor Green

# Run the Python module
python src\cli\main.py

# Keep window open so user can see results
if ($LASTEXITCODE -eq 0) {
    Write-Host "Press any key to exit..." -ForegroundColor Cyan
    $null = $Host.UI.RawUI.ReadKey()
}
