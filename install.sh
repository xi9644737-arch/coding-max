#!/bin/bash
# coding-max + coding-pipeline 安装脚本 (macOS/Linux)
# 用法: curl -fsSL https://raw.githubusercontent.com/xi9644737-arch/coding-max/master/install.sh | bash

REPO="https://github.com/xi9644737-arch/coding-max.git"
TMP=$(mktemp -d)
SKILLS_DIR="${HOME}/.claude/skills"

echo "正在安装 coding-max + coding-pipeline..."
git clone --depth 1 "$REPO" "$TMP"

cp -r "$TMP/coding-max" "$SKILLS_DIR/coding-max"
cp -r "$TMP/coding-pipeline" "$SKILLS_DIR/coding-pipeline"
rm -rf "$TMP"

echo "完成！"
echo "  coding-max:      $SKILLS_DIR/coding-max"
echo "  coding-pipeline: $SKILLS_DIR/coding-pipeline"
