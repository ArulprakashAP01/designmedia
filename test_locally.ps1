# Install required Python packages
pip install requests packaging

# Run the dependency checker
python .github/scripts/check_dependencies.py

# Display the results
Write-Host "`nResults from dependency-report.json:"
Get-Content dependency-report.json | ConvertFrom-Json | ConvertTo-Json -Depth 10 