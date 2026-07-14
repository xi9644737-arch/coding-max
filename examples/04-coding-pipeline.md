# 示例: coding-pipeline — Monorepo 搭测试管道

## 场景

Monorepo 包含 `packages/web`（Node.js）和 `packages/api`（Python），两者都没有可运行测试。`coding-max` 判断风险不低，在 `.project-memory/PHASE.json` 写入 `bootstrapping` 后交给 `coding-pipeline`。

## 执行

1. 审计根目录和每个子包的 manifest、锁文件、既有测试、CI 与命令。
2. 先验证仓库自带命令；缺失时为每个子包选择一个最小原生测试框架。
3. 使用 `references/smoke-templates.md` 做无需依赖或低成本预检，不复制过时正则。
4. 相关依赖获授权且锁版本后，运行真实测试并取得可重复基线。
5. 根据目标平台选择 GitHub Actions、GitLab CI 或通用模板；Monorepo 用矩阵覆盖子项目和工具链版本。
6. 只记录真实测得的覆盖率；无法测量写 `unknown`。
7. 写 Pipeline 报告与索引，将 `PHASE.json` 更新为 `testing`，交回 `coding-max` 完成修复验证。

## 输出摘要

```text
测试基建已可运行：
- packages/web：测试命令与 CI job 已验证
- packages/api：测试命令与 CI job 已验证
- 覆盖率：记录真实输出；未测项为 unknown
- PHASE：testing
- 报告：.project-memory/pipelines/PIPELINE-YYYY-MM-DD-monorepo.md

coding-max 可继续执行回归测试和修复终审。
```
