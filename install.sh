#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <skills-directory>" >&2
  exit 2
fi

REPO="https://github.com/xi9644737-arch/coding-max.git"
TMP="$(mktemp -d)"
SKILLS_DIR="$1"

cleanup() { rm -rf -- "$TMP"; }
trap cleanup EXIT

git clone --depth 1 "$REPO" "$TMP"
mkdir -p "$SKILLS_DIR"
backup_root="$(dirname "$SKILLS_DIR")/.skill-backups/$(date +%Y%m%d-%H%M%S)"

for name in coding-max coding-pipeline; do
  target="$SKILLS_DIR/$name"
  if [[ -d "$target" ]]; then
    mkdir -p "$backup_root"
    cp -R "$target" "$backup_root/$name"
    rm -rf -- "$target"
  fi
  cp -R "$TMP/$name" "$target"
  echo "Installed: $target"
done
