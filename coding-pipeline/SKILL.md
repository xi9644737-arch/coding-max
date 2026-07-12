---
name: coding-pipeline
description: 当项目缺少测试、需要CI流水线、配置覆盖率基线、或coding-max探测到"无测试"时使用。支持Monorepo。触发:搭测试/配CI/加覆盖率/测试基建/github actions/monorepo。
---

# coding-pipeline

给项目搭测试管道。**只通管道，不写业务测试**。CI 能跑 + 冒烟通过 + 增量覆盖率基线有就行。业务测试留给 `coding-max` 修 bug 时逐个填。

## 联动

coding-max 无测试→拦截→写PHASE(`bootstrap`)→本skill搭管道→清PHASE→回coding-max步骤6。PHASE锁防AI记忆丢失。用户也可独立召唤:`"帮我搭测试"`。渐进式补全:审计缺什么补什么—全无/缺CI/缺覆盖率/全有→各自对应。

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

### 2. 脚手架（纯静态冒烟测试）

**不实际import。** 用语法树解析做纯静态检查——避免入口连数据库/读.env/初始化日志炸CI：

```python
# tests/test_smoke.py
import ast
def test_entry_syntax():
    with open("app/main.py") as f: tree = ast.parse(f.read())
    assert tree is not None

def test_no_bare_except():
    with open("app/main.py") as f: tree = ast.parse(f.read())
    for n in ast.walk(tree):
        if isinstance(n, ast.ExceptHandler):
            assert n.type is not None, f"裸except L{n.lineno}"
```

Python用`ast.parse`,JS/TS用`acorn`,Go用`go/parser`。跑语法树,不导入。

### 3. 生成 CI(仅GitHub Actions)
`.github/workflows/test.yml`:push+PR触发,矩阵(Python多版本/Node LTS/Go stable),checkout→装依赖→跑测试→上传覆盖率,不设硬阈值,按lock文件hash缓存。Monorepo→每子包独立job。

### 4. 增量覆盖率基线
不用全局%,用git diff追增量:`git diff HEAD~1 --name-only`→只算变更文件的新增/修改行。写入PROJECT_PROFILE:`增量覆盖率:84%(diff行45/38)`+`全局:12%(仅参考)`。coding-max步骤6只比增量是否≥基线,重构删死代码不阻塞。

### 5. Pre-commit(可选)
问用户是否加hook(跑变更模块测试,不全量)。

## 输出

```
✅ 管道已通: Python/pytest + CI + 增量基线84% → PHASE已清 → 回coding-max
```

## 硬约束
1.不写业务测试 2.冒烟=语法树(不import) 3.不装全局CLI 4.CI跑通再提交 5.增量覆盖率,不卡全局% 6.已有框架不重复装 7.已有CI不覆盖 8.Phase1:Python/Node/Go,其他通用模板 9.审计用文件工具不用shell 10.Monorepo递归子包独立
