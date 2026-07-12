---
name: coding-pipeline
description: 当项目缺少测试、需要CI流水线、配置覆盖率基线、或coding-max探测到"无测试"时使用。支持Monorepo。触发:搭测试/配CI/加覆盖率/测试基建/github actions/monorepo。
---

# coding-pipeline

给项目搭测试管道。**只通管道，不写业务测试**。CI 能跑 + 冒烟通过 + 增量覆盖率基线有就行。业务测试留给 `coding-max` 修 bug 时逐个填。

## 联动

coding-max 无测试→拦截→写PHASE.json(`state:bootstrapping`)→本skill搭管道→状态→`testing`→回coding-max步骤6。PHASE.json状态机防AI记忆丢失。用户也可独立召唤:`"帮我搭测试"`。渐进式补全:审计缺什么补什么—全无/缺CI/缺覆盖率/全有→各自对应。

## 流程

### 0. 审计
用文件工具探测(Glob/Grep/Read,不用shell),不限根目录,递归子包:

| 审计结果 | 行动 |
|---------|------|
| 全无 | 装框架→脚手架→CI→基线 |
| 有框架无CI | 只生成`.github/workflows/test.yml` |
| 有框架+CI无覆盖率 | 只改配置加cov参数+跑基线 |
| 全有 | 输出现状报告 |

Monorepo:递归`packages/`/`services/`/`apps/`→每子包独立审计→矩阵输出。

### 1. 装框架（如需）

| 语言 | 检测 | 框架 |
|------|------|------|
| Python | `pyproject.toml` | pytest+pytest-cov |
| Node/TS | `package.json` | vitest(vite)/jest(其他) |
| Go | `go.mod` | testing(标准库) |

其他语言→通用Docker+Bash CI模板+"手动改,欢迎PR"。

### 2. 脚手架（两阶段冒烟测试）

**Phase1: 纯语法（秒级，不装依赖）**

用语法树解析做纯静态检查——避免入口连数据库/读.env/初始化日志炸CI。**不需要装项目依赖**，只跑语言内置 parser。

| 语言 | 工具 | 安装 |
|------|------|------|
| Python | `ast.parse` | 内置,无需安装 |
| Node/TS | `acorn` 或 `fs.readFileSync`+正则 | `npx acorn`(按需)或纯正则 |
| Go | `go/parser` | 内置 |

Phase1 模板（Python 示例）：
```python
# tests/test_smoke.py — Phase1: 纯语法,不import项目代码
import ast, os, sys
SRC = os.path.join(os.path.dirname(__file__), "..", "app")

def test_syntax():
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
                            assert not isinstance(d, (ast.List, ast.Dict, ast.Set)), f"可变默认 {f}:{d.lineno}"
```

**快速生成**: `coding-pipeline --init-smoke <src_dir>` 自动扫描源码目录生成上述模板，无需手写。

**Phase2: 完整测试（装依赖后）**

CI 在 Phase1 通过后安装项目依赖，跑真正的 import + 业务测试（由 `coding-max` 步骤3 TDD 逐个补充）。Phase1 失败→不进入 Phase2，省 CI 时间。

### 3. 生成 CI（多平台）

探测已有 CI 配置，补缺失平台。不覆盖已有配置。

| 平台 | 配置文件 | 生成条件 |
|------|---------|---------|
| GitHub Actions | `.github/workflows/test.yml` | 无已有CI配置→默认生成 |
| GitLab CI | `.gitlab-ci.yml` | 用户指定或项目根已有`.gitlab-ci.yml`(补全) |

**CI 模板结构**（平台无关）: Phase1=纯语法(秒级,无依赖)→Phase2=装依赖+业务测试+覆盖率。Monorepo→每子包独立job。

GitHub Actions 模板:
```yaml
# .github/workflows/test.yml
jobs:
  phase1-smoke:
    steps: [checkout, setup-language, run-smoke-tests(no-deps)]
  phase2-test:
    needs: phase1-smoke  # Phase1 失败→跳过 Phase2
    steps: [checkout, setup-language, cache-deps, install-deps, run-tests, upload-coverage]
```

GitLab CI 模板:
```yaml
# .gitlab-ci.yml
stages: [smoke, test]

smoke:
  stage: smoke
  script: [setup-language, run-smoke-tests(no-deps)]

test:
  stage: test
  needs: [smoke]
  script: [install-deps, run-tests, upload-coverage]
  artifacts: { reports: { coverage_report: ... } }
```

通用参数：push+PR/MR触发, 语言版本矩阵, 不设硬覆盖率阈值, 按 lock 文件 hash 缓存。

### 4. 增量覆盖率基线
不用全局%,用git diff追增量:`git diff HEAD~1 --name-only`→只算变更文件的新增/修改行。写入PROJECT_PROFILE:`增量覆盖率:84%(diff行45/38)`+`全局:12%(仅参考)`。coding-max步骤6只比增量是否≥基线,重构删死代码不阻塞。

### 5. Pre-commit(可选)
问用户是否加hook(跑变更模块测试,不全量)。

## 输出

```
✅ 管道已通: Python/pytest + GitLab CI + GHA + 两段冒烟 + 增量基线84% → PHASE→testing → 回coding-max
```

## 硬约束
1.不写业务测试 2.Phase1冒烟=语法树(不import,不装依赖) 3.Phase2才装依赖跑业务测试 4.不装全局CLI 5.CI跑通再提交 6.增量覆盖率,不卡全局% 7.已有框架不重复装 8.已有CI不覆盖(可补缺失平台) 9.Phase1:Python/Node/Go,其他通用模板 10.审计用文件工具不用shell 11.Monorepo递归子包独立 12.多平台:GHA默认+GitLab CI可选

## 参考
- `references/gitlab-ci-template.yml` — GitLab CI 两阶段模板
- `coding-max` — 配套skill:修bug→TDD补业务测试
