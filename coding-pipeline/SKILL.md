---
name: coding-pipeline
description: Bootstrap or repair test infrastructure, CI, coverage baselines, and pre-commit for projects and Monorepos. Use when tests or CI are missing or broken, pipelines fail, coverage is unknown, or coding-max needs a trustworthy verification path.
---

# coding-pipeline

建立可验证的测试管道；冒烟不代替业务测试，不夸大本地或远程结果。

## 边界与状态

任务根：用户明确目录 > 最近 manifest/config > Git 根。递归排除依赖、vendor、构建与缓存目录。逐包审计 Monorepo，任一失败不得被汇总成功掩盖。

共用任务根 `.project-memory/PHASE.json`：`idle→bootstrapping→testing→done|failed`。旧任务结束后可保留报告并重置；不同 target 仍活动时不得覆盖。仅实际观察远程 CI 成功才写 `remote`，否则最多 `local`。细节和报告格式读取 `references/pipeline-workflow.md`。

## 路由

- **只审计**：读取 pipeline workflow；输出逐包成熟度与差距，不改文件。
- **搭/修本地测试**：再读 `references/smoke-templates.md`，只选择目标语言部分。
- **GitHub Actions**：再读 `references/github-actions-ci-template.yml`。
- **GitLab CI**：再读 `references/gitlab-ci-template.yml`。
- **其他平台/语言**：再读 `references/universal-ci-template.yml`。
- **架构门禁**：仅在 `../coding-untangle/SKILL.md` 已给出可执行边界时，实现最小测试/lint/CI gate；不得自行决定架构。

不要同时加载无关语言或 CI 平台 reference。

## 完成条件

静态预检、工具链预检、真实测试退出码和生成 CI 语法均按任务范围验证；模板无占位、示例路径、未使用变量或假通过命令。覆盖率无可靠来源写 `unknown`。远程未运行只能写“已配置、待验证”。

完成后更新 `PROJECT_PROFILE.md`、`pipelines/PIPELINE-日期-slug.md`、`PIPELINES.md` 和 PHASE。失败重试必须换证据视角，第三次写 `failed` 和报告路径。

## 硬约束

不让冒烟冒充回归；不覆盖现有框架/CI/用户改动；不安装用户全局 CLI；不伪造覆盖率、依赖可复现性或远程状态；外部集成必须已有配置或获授权。单 Agent 完整执行，不绑定子代理、模型或 MCP。

## 按需资源

- 审计、框架、状态、验证、报告：`references/pipeline-workflow.md`
- 五语言预检：`references/smoke-templates.md`
- GitHub Actions：`references/github-actions-ci-template.yml`
- GitLab CI：`references/gitlab-ci-template.yml`
- 其他平台：`references/universal-ci-template.yml`
- Bug/TDD：`../coding-max/SKILL.md`
- 耦合边界与疫苗定义：`../coding-untangle/SKILL.md`
