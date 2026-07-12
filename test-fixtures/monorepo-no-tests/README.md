# monorepo-no-tests

测试 `coding-pipeline` + `coding-max` 联动的 Monorepo。

## 结构

```
packages/
├── api/     Python/FastAPI  → 无测试, 无 CI
└── web/     Node.js/Next.js → 无测试, 无 CI
```

## 测试方式

复制到你的项目目录，对 AI 说：

> "这个项目有个 bug，packages/api 的 /users 接口没有做参数校验"

观察：
1. coding-max 步骤 0.0 是否拦截"无测试"
2. 是否提示启动 coding-pipeline
3. coding-pipeline 是否递归扫描到两个子包
4. 是否生成两个独立的 CI job
5. 是否生成语法树冒烟测试（不实际 import FastAPI/React）
6. PHASE 锁是否正常写入和清除
7. 回 coding-max 后步骤 6 是否从降级→正常
