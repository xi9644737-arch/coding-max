# coding-max 安装脚本 (Windows PowerShell)
# 用法: irm https://raw.githubusercontent.com/xi9644737-arch/coding-max/master/install.ps1 | iex

$repo = "https://github.com/xi9644737-arch/coding-max.git"
$target = "$env:USERPROFILE\.claude\skills\coding-max"

if (Test-Path $target) {
    Write-Host "coding-max 已安装，正在更新..." -ForegroundColor Yellow
    git -C $target pull
} else {
    Write-Host "正在安装 coding-max..." -ForegroundColor Green
    New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null
    git clone $repo $target
}

Write-Host "完成！路径: $target" -ForegroundColor Green
