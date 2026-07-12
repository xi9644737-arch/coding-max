#!/bin/bash
# coding-max 安装脚本 (macOS/Linux)
# 用法: curl -fsSL https://raw.githubusercontent.com/xi9644737-arch/coding-max/master/install.sh | bash

REPO="https://github.com/xi9644737-arch/coding-max.git"
TARGET="${HOME}/.claude/skills/coding-max"

if [ -d "$TARGET" ]; then
    echo "coding-max 已安装，正在更新..."
    git -C "$TARGET" pull
else
    echo "正在安装 coding-max..."
    mkdir -p "$(dirname "$TARGET")"
    git clone "$REPO" "$TARGET"
fi

echo "完成！路径: $TARGET"
