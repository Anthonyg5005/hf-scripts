# Prompt user for the number of models to download
$numberOfModels = Read-Host "Enter the number of models to download"

# Initialize an array to store model repos
$modelRepos = @()

# Loop to collect model repos
for ($i = 1; $i -le $numberOfModels; $i++) {
    $modelRepo = Read-Host "Enter Model Repo $i"
    $modelRepos += $modelRepo
}

# Function to download a model in a new PowerShell window
function Get-Model {
    param (
        [string]$modelRepo
    )

    # Start a new PowerShell window and execute the download-model.py script
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -Command .\venv\Scripts\activate.ps1; python.exe download-model.py $modelRepo" -NoNewWindow
}

# Loop through each model repo and download in a new PowerShell window
foreach ($repo in $modelRepos) {
    Get-Model -modelRepo $repo
}

Write-Host "Downloads initiated for $numberOfModels models. Check the progress in the new PowerShell windows."
