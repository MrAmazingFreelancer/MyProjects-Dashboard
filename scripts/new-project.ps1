param(
    [Parameter(Mandatory = $true)]
    [string]$Name,
    [string]$BasePath = "D:\Projects"
)

$templatePath = "D:\xampp\htdocs\_templates\project-root"
if (!(Test-Path $templatePath)) {
    throw "Template path not found: $templatePath"
}

if (!(Test-Path $BasePath)) {
    New-Item -ItemType Directory -Path $BasePath | Out-Null
}

$targetPath = Join-Path $BasePath $Name
if (Test-Path $targetPath) {
    throw "Target already exists: $targetPath"
}

Copy-Item -Path $templatePath -Destination $targetPath -Recurse
Write-Output "Created project scaffold at: $targetPath"
Write-Output "Open in browser via: http://localhost/projects/$Name/"
