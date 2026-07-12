# coding-max + coding-pipeline 安装脚本 (Windows PowerShell)
# 用法: irm https://raw.githubusercontent.com/xi9644737-arch/coding-max/master/install.ps1 | iex

$repo = "https://github.com/xi9644737-arch/coding-max.git"
$tmp = Join-Path $env:TEMP "coding-max-install"
$skills = "$env:USERPROFILE\.claude\skills"

Write-Host "正在安装 coding-max + coding-pipeline..." -ForegroundColor Green

if (Test-Path $tmp) { Remove-Item -Recurse -Force $tmp }
git clone --depth 1 $repo $tmp | Out-Null

New-Item -ItemType Directory -Force -Path $skills | Out-Null
Copy-Item -Recurse "$tmp\coding-max" "$skills\coding-max" -Force
Copy-Item -Recurse "$tmp\coding-pipeline" "$skills\coding-pipeline" -Force
Remove-Item -Recurse -Force $tmp

Write-Host "完成！" -ForegroundColor Green
Write-Host "  coding-max:      $skills\coding-max"
Write-Host "  coding-pipeline: $skills\coding-pipeline"
