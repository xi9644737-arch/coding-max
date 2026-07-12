# 冒烟测试模板 (Phase1: 纯静态, 不import, 不装依赖)

## Python (`ast.parse`, 内置)

```python
# tests/test_smoke.py
import ast, os
SRC = os.path.join(os.path.dirname(__file__), "..", "app")

def test_all_syntax():
    """每个.py文件能被ast.parse解析"""
    for f in os.listdir(SRC):
        if f.endswith(".py"):
            with open(os.path.join(SRC, f)) as fh:
                assert ast.parse(fh.read()) is not None

def test_no_bare_except():
    """禁裸except:"""
    for f in os.listdir(SRC):
        if f.endswith(".py"):
            with open(os.path.join(SRC, f)) as fh:
                for n in ast.walk(ast.parse(fh.read())):
                    if isinstance(n, ast.ExceptHandler):
                        assert n.type is not None, f"裸except {f}:{n.lineno}"

def test_no_mutable_defaults():
    """禁可变默认参数"""
    for f in os.listdir(SRC):
        if f.endswith(".py"):
            with open(os.path.join(SRC, f)) as fh:
                for n in ast.walk(ast.parse(fh.read())):
                    if isinstance(n, ast.FunctionDef):
                        for d in n.args.defaults:
                            assert not isinstance(d, (ast.List,ast.Dict,ast.Set)), f"可变默认 {f}:{d.lineno}"

def test_init_py():
    """每个子包有__init__.py"""
    for root, dirs, files in os.walk(SRC):
        if files and not any(f.endswith('.py') for f in files):
            continue
        if '__init__.py' not in files:
            assert False, f"缺少__init__.py: {root}"
```

## Node.js (`fs.readFileSync` + 正则, 内置)

```js
// tests/smoke.test.js — 跑在 vitest/jest, 不 import 项目代码
const fs = require('fs');
const path = require('path');
const src = path.join(__dirname, '..', 'src');

test('entry files exist and are non-empty', () => {
  const files = fs.readdirSync(src).filter(f => /\.(ts|js)$/.test(f));
  expect(files.length).toBeGreaterThan(0);
  for (const f of files) {
    const content = fs.readFileSync(path.join(src, f), 'utf-8');
    expect(content.length).toBeGreaterThan(10);
  }
});

test('no bare catch blocks', () => {
  for (const f of walkSync(src).filter(f => /\.(ts|js)$/.test(f))) {
    const content = fs.readFileSync(f, 'utf-8');
    // 匹配 catch 后无类型标注
    const bareCatches = content.match(/catch\s*\(\s*\w*\s*\)\s*\{/g);
    expect(bareCatches).toBeNull();
  }
});

test('imports resolve statically', () => {
  for (const f of walkSync(src).filter(f => /\.(ts|js)$/.test(f))) {
    const content = fs.readFileSync(f, 'utf-8');
    const imports = content.match(/from\s+['"]([^'"]+)['"]/g) || [];
    for (const imp of imports) {
      const p = imp.match(/from\s+['"]([^'"]+)['"]/)[1];
      if (p.startsWith('.') && !p.endsWith('.css') && !p.endsWith('.svg')) {
        // 相对路径 import 的目标文件应存在
        const dir = path.dirname(f);
        const target = path.resolve(dir, p);
        expect(() => fs.accessSync(target + '.ts') || fs.accessSync(target + '.js') || fs.accessSync(target + '/index.ts') || fs.accessSync(target + '/index.js')).not.toThrow();
      }
    }
  }
});

function* walkSync(dir) {
  for (const f of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, f.name);
    if (f.isDirectory() && f.name !== 'node_modules') yield* walkSync(p);
    else yield p;
  }
}
```

## Go (`go vet` + `go build`, 内置)

```bash
# Phase1: go内置检查，无需额外测试文件
go vet ./...
go build ./...
```

Go项目Phase1用内置工具链，不装额外linter。仅在`go vet`/`go build`都通过后才进Phase2。

## Rust (`cargo check` + `cargo clippy`, 需clippy组件)

```bash
# Phase1: 类型检查(不生成二进制) + lint
rustup component add clippy
cargo check          # 全workspace类型检查，秒级
cargo clippy -- -D warnings   # lint硬错误，有warning就失败
```

不需要写额外测试文件。`cargo check`跳过代码生成，比`cargo build`快5-10倍。Phase1通过后Phase2跑`cargo test`。

## Java/Kotlin (`mvn compile` / `gradle compileJava` + Checkstyle)

```bash
# Phase1: 编译检查(不跑测试) + 可选lint
# Maven:
mvn compile -q
mvn checkstyle:check   # 如已配置checkstyle插件

# Gradle:
./gradlew compileJava compileTestJava
./gradlew checkstyleMain checkstyleTest   # 如已配置
```

不需要写额外测试文件。编译成功=语法正确+类型正确+依赖可解析。Phase2再跑`mvn test`/`gradle test`。
