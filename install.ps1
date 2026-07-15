param(
    [Parameter(Mandatory = $true)]
    [string]$Destination
)

$ErrorActionPreference = "Stop"
$repo = "https://github.com/xi9644737-arch/coding-max.git"
$tmp = Join-Path $env:TEMP ("coding-max-install-" + [Guid]::NewGuid().ToString("N"))
$skills = [System.IO.Path]::GetFullPath($Destination)

try {
    git clone --depth 1 $repo $tmp | Out-Null
    $version = (Get-Content -Raw -LiteralPath (Join-Path $tmp "VERSION")).Trim()
    New-Item -ItemType Directory -Force -Path $skills | Out-Null
    $backupRoot = Join-Path (Split-Path -Parent $skills) (".skill-backups\" + (Get-Date -Format "yyyyMMdd-HHmmss"))

    foreach ($name in @("coding-max", "coding-untangle", "coding-pipeline")) {
        $target = Join-Path $skills $name
        if (Test-Path -LiteralPath $target) {
            New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null
            Copy-Item -Recurse -Force -LiteralPath $target -Destination (Join-Path $backupRoot $name)
            Remove-Item -Recurse -Force -LiteralPath $target
        }
        Copy-Item -Recurse -Force -LiteralPath (Join-Path $tmp $name) -Destination $target
        Write-Host "Installed $name ($version): $target" -ForegroundColor Green
    }
}
finally {
    if (Test-Path -LiteralPath $tmp) {
        Remove-Item -Recurse -Force -LiteralPath $tmp
    }
}
