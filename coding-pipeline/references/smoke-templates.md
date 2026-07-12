# 冒烟测试模板（Phase1: 纯语法,不import,不装依赖）

## Python (`ast.parse`, 内置)

```python
# tests/test_smoke.py
import ast, os
SRC = os.path.join(os.path.dirname(__file__), "..", "app")

def test_all_syntax():
    for f in os.listdir(SRC):
        if f.endswith(".py"):
            with open(os.path.join(SRC, f)) as fh:
                assert ast.parse(fh.read()) is not None

def test_no_bare_except():
    for f in os.listdir(SRC):
        if f.endswith(".py"):
            with open(os.path.join(SRC, f)) as fh:
                for n in ast.walk(ast.parse(fh.read())):
                    if isinstance(n, ast.ExceptHandler):
                        assert n.type is not None, f"裸except {f}:{n.lineno}"

def test_no_mutable_defaults():
    for f in os.listdir(SRC):
        if f.endswith(".py"):
            with open(os.path.join(SRC, f)) as fh:
                for n in ast.walk(ast.parse(fh.read())):
                    if isinstance(n, ast.FunctionDef):
                        for d in n.args.defaults:
                            assert not isinstance(d, (ast.List,ast.Dict,ast.Set)), f"可变默认 {f}:{d.lineno}"
```

## Node.js (`fs.readFileSync` + 正则, 内置)

```js
// tests/smoke.test.js — 跑在 vitest/jest, 但不 import 项目代码
const fs = require('fs');
const path = require('path');
const src = path.join(__dirname, '..', 'src');

test('entry exists and is non-empty', () => {
  const files = fs.readdirSync(src).filter(f => f.endsWith('.ts'));
  expect(files.length).toBeGreaterThan(0);
});

test('no bare catch blocks', () => {
  for (const f of fs.readdirSync(src).filter(f => f.endsWith('.ts'))) {
    const content = fs.readFileSync(path.join(src, f), 'utf-8');
    expect(content).not.toMatch(/catch\s*\(\s*\w*\s*\)\s*\{\s*\}/g);
  }
});
```

## Go (`go vet` + `go build`, 内置)

```bash
# Phase1: 不需要写额外测试文件, go vet 内置检查
go vet ./...
go build ./...
```
