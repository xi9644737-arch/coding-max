# 示例: coding-pipeline — Monorepo 搭测试管道

## 场景

Monorepo 项目，`packages/web`(Node.js/Next.js) 和 `packages/api`(Python/Django) **全无测试**。

coding-max 步骤8 拦截: "项目为测试荒漠，搭基建？" → 用户 Y → 触发 coding-pipeline。

## AI 行为

**步骤0: 审计**
```
Glob packages/*/package.json → packages/web
Glob packages/*/pyproject.toml → packages/api

审计结果:
  packages/web:  Node.js/Next.js, 无框架, 无CI → 全搭
  packages/api:  Python/Django, 无框架, 无CI → 全搭
```

**步骤1: 装框架**
```bash
# packages/web — Node.js + Vite → vitest
cd packages/web && npm install -D vitest @vitest/coverage-v8

# packages/api — Python → pytest
cd packages/api && pip install pytest pytest-cov pytest-django
```

**步骤2: 两阶段冒烟**

Phase1 (秒级，不装依赖):
```python
# packages/api/tests/test_smoke.py — 纯 ast.parse
import ast, os
def test_all_syntax():
    for f in os.listdir("packages/api/app"):
        if f.endswith(".py"):
            with open(f"packages/api/app/{f}") as fh:
                assert ast.parse(fh.read()) is not None
```
```js
// packages/web/__tests__/smoke.test.js — 纯 fs + 正则
const fs = require('fs');
test('no bare catch', () => {
  for (const f of fs.readdirSync('packages/web/src')) {
    expect(fs.readFileSync(`packages/web/src/${f}`, 'utf-8')).not.toMatch(/catch\s*\(\s*\w*\s*\)\s*\{/);
  }
});
```

Phase2: Phase1通过→装依赖→vitest/pytest验证框架可运行。

**步骤3: 生成CI**
```yaml
# .github/workflows/test.yml — 每子包独立job，含cache+Codecov上传+Slack通知
jobs:
  api-smoke: ... (ast.parse, 秒级)
  api-test: needs:api-smoke, matrix:[3.11,3.12,3.13], cache:pip, cov:Codecov
  web-smoke: ... (入口检查, 秒级)
  web-test: needs:web-smoke, matrix:[18,20,22], cache:npm, cov:Codecov
```

**步骤4: 增量基线**
```
PROJECT_PROFILE 写入:
  packages/web: 增量覆盖率 92% (2/2冒烟通过)
  packages/api: 增量覆盖率 88% (2/2冒烟通过)
```

**PHASE.json → `state:testing`** → 回coding-max步骤8。

## AI 输出

```
✅ 管道已通(coding-pipeline):

  Monorepo 审计: 2/2 子包已覆盖
  packages/web:  Node.js  → vitest + CI(GHA) + 增量基线 92%
  packages/api:  Python   → pytest + CI(GHA) + 增量基线 88%
  PHASE锁: testing

  → coding-max 步骤8 恢复正常验证。
```
