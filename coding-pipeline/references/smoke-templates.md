# 分层预检与冒烟模板

## 目录

1. Python 静态预检
2. JavaScript/TypeScript 静态预检
3. Go 工具链预检
4. Rust 工具链预检
5. Java/Kotlin 工具链预检

这些片段必须适配真实源码目录。静态预检不安装包；工具链预检可能解析或下载项目已声明的依赖，报告时要区分。

## 1. Python 静态预检

使用标准库递归解析语法，并拒绝真正的裸 `except:`。不要强制所有目录包含 `__init__.py`，因为 namespace package 合法。

```python
from __future__ import annotations

import ast
from pathlib import Path

SOURCE_ROOTS = [Path("app"), Path("src")]
files = [
    path
    for root in SOURCE_ROOTS
    if root.exists()
    for path in root.rglob("*.py")
]
assert files, "未在配置的源码目录找到 Python 文件"

errors: list[str] = []
for path in files:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError) as exc:
        errors.append(f"{path}: {exc}")
        continue
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            errors.append(f"{path}:{node.lineno}: bare except")

assert not errors, "\n".join(errors)
print(f"Python static preflight passed: {len(files)} files")
```

可变默认参数等风格规则优先交给项目已有 Ruff/Pylint，不在零依赖脚本里复制完整 linter。

## 2. JavaScript/TypeScript 静态预检

不要用 `catch(e) {` 正则判断“裸 catch”：这是合法且常见的错误绑定。零依赖阶段对 JavaScript 使用 `node --check`，并用候选路径检查相对 import；TypeScript 的语法和类型必须在依赖恢复后交给项目编译器。

```js
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

function walk(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    if (entry.name === 'node_modules') return [];
    const full = path.join(dir, entry.name);
    return entry.isDirectory() ? walk(full) : [full];
  });
}

const files = walk('src').filter((file) => /\.(cjs|mjs|js|jsx|ts|tsx)$/.test(file));
if (files.length === 0) throw new Error('未在 src 找到 JS/TS 文件');

for (const file of files.filter((name) => /\.(cjs|mjs|js)$/.test(name))) {
  const result = spawnSync(process.execPath, ['--check', file], { encoding: 'utf8' });
  if (result.status !== 0) throw new Error(`${file}: ${result.stderr}`);
}

const importPattern = /(?:from\s+|import\s*\()['"]([^'"]+)['"]/g;
for (const file of files) {
  const source = fs.readFileSync(file, 'utf8');
  for (const match of source.matchAll(importPattern)) {
    const specifier = match[1];
    if (!specifier.startsWith('.')) continue;
    const target = path.resolve(path.dirname(file), specifier);
    const candidates = [
      target,
      ...['.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.json'].map((ext) => target + ext),
      ...['index.ts', 'index.tsx', 'index.js', 'index.jsx'].map((name) => path.join(target, name)),
    ];
    if (!candidates.some((candidate) => fs.existsSync(candidate))) {
      throw new Error(`${file}: unresolved relative import ${specifier}`);
    }
  }
}

console.log(`JS/TS static preflight passed: ${files.length} files`);
```

依赖恢复后运行项目已有的 `tsc --noEmit`、Vitest 或 Jest。不要全局安装 TypeScript。

## 3. Go 工具链预检

```bash
go vet ./...
go build ./...
go test ./...
```

`go vet/build` 可能下载 `go.mod` 已声明模块。测试框架默认使用标准库 `testing`，不要仅为搭管道引入 testify。

## 4. Rust 工具链预检

```bash
cargo check --workspace
cargo clippy --workspace -- -D warnings
cargo test --workspace
```

仅当当前 toolchain 已有 clippy 时在预检中运行；缺失组件属于环境准备，不得声称“零安装”。覆盖率工具沿用项目已有配置。

## 5. Java/Kotlin 工具链预检

Maven：

```bash
mvn -B -q compile
mvn -B test
```

Gradle：

```bash
./gradlew compileJava compileTestJava
./gradlew test
```

编译会解析构建文件声明的依赖。只有已配置 Checkstyle/JaCoCo 时直接运行；否则把新增插件作为显式管道改动并验证。
