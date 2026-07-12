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

| 语言 | 检测 | 框架 | 说明 |
|------|------|------|------|
| Python | `pyproject.toml` | pytest+pytest-cov | 完整生态,断言/夹具/覆盖率 |
| Node/TS | `package.json` | vitest(vite)/jest(其他) | vitest快,jest生态广 |
| Go | `go.mod` | testing + testify | 标准库只有函数签名,需 testify 补断言+覆盖率 |

Go 需额外安装 `github.com/stretchr/testify`。Phase1 用 `go vet` + `go build ./...` 做静态检查。

其他语言→通用 Docker+Bash 模板（见 `references/universal-ci-template.yml`），装对应测试框架。

### 2. 脚手架（两阶段冒烟测试）

**Phase1**: 纯语法树检查，**不装项目依赖**，秒级反馈。Python用`ast.parse`(内置), Node用正则/`acorn`, Go用`go/parser`(内置)。模板见`references/smoke-templates/`。

**Phase2**: Phase1通过后装依赖，跑业务测试（由`coding-max`步骤3 TDD补）。Phase1失败→跳过Phase2省CI时间。

### 3. 生成 CI（多平台）

探测已有 CI→补缺失平台。结构：Phase1(纯语法)→Phase2(装依赖+业务测试)。Monorepo→每子包独立job。

| 平台 | 文件 | 生成条件 | 模板 |
|------|------|---------|------|
| GitHub Actions | `.github/workflows/test.yml` | 无已有CI→默认 | `references/`下示例 |
| GitLab CI | `.gitlab-ci.yml` | 用户指定 | `references/gitlab-ci-template.yml` |

通用参数：push+PR/MR, 语言版本矩阵, 不设硬阈值, lock文件hash缓存。

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
- `references/smoke-templates.md` — Phase1冒烟模板(Python/Node/Go)
- `references/gitlab-ci-template.yml` — GitLab CI 两阶段模板
- `references/universal-ci-template.yml` — 通用模板(Rust/Java/Ruby/PHP/...)
- `coding-max` — 配套skill
