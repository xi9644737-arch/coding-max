# 示例：coding-pipeline — Monorepo 搭测试管道

## 场景

Monorepo 项目，`packages/web`(Node.js) 和 `packages/api`(Python) 全无测试。

coding-max 步骤 0.0 拦截："项目为测试荒漠，是否先搭测试基建？" → 用户 Y → 触发 coding-pipeline。

## AI 行为

**步骤 0：审计**

```
Glob packages/*/package.json → 命中 packages/web
Glob packages/*/pyproject.toml → 命中 packages/api

审计结果:
  packages/web:  Node.js/Next.js, 无测试框架, 无CI → 全搭
  packages/api:  Python/Django, 无测试框架, 无CI → 全搭
```

**步骤 1：装框架**
```bash
# packages/web
cd packages/web && npm install -D vitest

# packages/api
cd packages/api && pip install pytest pytest-cov pytest-django
```

**步骤 2：脚手架（纯语法树冒烟测试）**
```python
# packages/api/tests/test_smoke.py
import ast

def test_entry_syntax():
    with open("packages/api/app/main.py") as f:
        tree = ast.parse(f.read())
    assert tree is not None
```

```typescript
// packages/web/__tests__/smoke.test.ts
import { describe, it, expect } from 'vitest'
import * as acorn from 'acorn'
import * as fs from 'fs'

describe('entry syntax', () => {
  it('parses without error', () => {
    const code = fs.readFileSync('packages/web/src/index.ts', 'utf-8')
    expect(() => acorn.parse(code, { ecmaVersion: 2022 })).not.toThrow()
  })
})
```

**步骤 3：生成 CI**
```yaml
# .github/workflows/test.yml — 每个子包独立 job
jobs:
  web:
    steps: [checkout, node 20, npm ci, cd packages/web && npx vitest run --coverage]
  api:
    steps: [checkout, python 3.12, pip install -r requirements.txt, cd packages/api && pytest --cov=. --cov-report=xml]
```

**步骤 4：增量覆盖率基线**

写入 PROJECT_PROFILE：
```
packages/web: 增量覆盖率 92% (2/2 冒烟通过)
packages/api: 增量覆盖率 88% (2/2 冒烟通过)
```

**PHASE 锁：清除。** 切回 coding-max。

## AI 输出

```
✅ 管道已通(coding-pipeline):

  Monorepo 审计: 2/2 子包已覆盖
  packages/web:  Node.js  → vitest + CI + 增量基线 92%
  packages/api:  Python   → pytest + CI + 增量基线 88%
  PHASE锁: 已清除

  → coding-max 步骤6 恢复正常模式。
```
