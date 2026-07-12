---
name: coding-pipeline
description: 给项目搭测试管道。触发:搭测试/配CI/加覆盖率/测试基建/github actions/monorepo。支持Monorepo。只通管道不写业务测试。
---

# coding-pipeline

给项目搭测试管道。**只通管道，不写业务测试。** CI能跑+冒烟通过+增量基线有=完工。业务测试留给 `coding-max` 修bug时逐个填。

## 联动

coding-max步骤8探测无测试→写 `PHASE.json(state:bootstrapping)`→本skill搭管道→`state:testing`→回coding-max。也可独立召唤: `"帮我搭测试"`。

## 流程

### 0. 审计 (Glob/Grep/Read，不用shell)

递归Monorepo子包 (`packages/`/`services/`/`apps/`):

| 审计结果 | 行动 |
|---------|------|
| 全无(框架+CI+覆盖率) | 装框架→冒烟→CI→基线 |
| 有框架无CI | 只生成CI |
| 有CI无覆盖率 | 只改配置+cov参数+跑基线 |
| 全有 | 输出健康报告 |

### 1. 装框架 (如需)

| 语言 | 检测文件 | 框架 | Phase1检查 |
|------|---------|------|-----------|
| Python | `pyproject.toml`/`setup.cfg` | pytest+pytest-cov | `ast.parse`语法+裸except+可变默认 |
| Node/TS | `package.json` | vitest(Vite)/jest(其他) | 入口存在+裸catch+import可解析 |
| Go | `go.mod` | testing+testify | `go vet`+`go build ./...` |
| Rust | `Cargo.toml` | cargo test+llvm-cov | `cargo check`+`cargo clippy -D warnings` |
| Java/Kotlin | `pom.xml`/`build.gradle` | JUnit5+JaCoCo | `mvn compile`/`gradle compileJava` |

其他语言→通用模板(`references/universal-ci-template.yml`)。

### 2. 两阶段冒烟

**Phase1** (秒级，不装依赖):

| 语言 | 检查项 |
|------|--------|
| Python | `ast.parse`→语法 + `ast.walk`→裸except/可变默认 + `os.path.exists`→`__init__.py` |
| Node/TS | `fs.readFileSync`→入口存在 + 正则→裸catch + `require.resolve`→核心import可解析 |
| Go | `go vet ./...` + `go build ./...`(内置，无需测试文件) |
| Rust | `cargo check`(类型检查，不生成二进制) + `cargo clippy -- -D warnings` |
| Java | `mvn compile`/`gradle compileJava` + Checkstyle(如已配置) |

**Phase2**: Phase1通过→装依赖→跑脚手架验证(框架能跑，不写业务断言)。Phase1失败→跳过Phase2。模板见 `references/smoke-templates.md`。

### 3. 生成CI

探测已有CI→补缺失。Monorepo→每子包独立job。

| 平台 | 文件 | 条件 |
|------|------|------|
| GitHub Actions | `.github/workflows/test.yml` | 无已有CI→默认 |
| GitLab CI | `.gitlab-ci.yml` | 用户指定/探测到 |

CI模板含:
- push+PR/MR触发
- 语言版本矩阵
- lock文件hash缓存(`actions/cache@v4`/`cache:key:`)
- Phase1→Phase2依赖(`needs`)
- 覆盖率上传步骤(Codecov/Coveralls action)
- 失败通知模板(Slack webhook，可选)

### 4. 增量基线 + Pre-commit

**增量覆盖率**: `git diff HEAD~1 --name-only`→只算变更文件新增/修改行。写入 `PROJECT_PROFILE`: `增量覆盖率:84%(diff行45/38)`+`全局:12%(仅参考)`。coding-max步骤8只比增量≥基线。

**Pre-commit**: 探测 `.pre-commit-config.yaml`→有则追加变更模块测试(不全量)；无则问是否安装。Python推荐`ruff`+`pytest`；Node推荐`lint-staged`+`vitest related`。

### 5. 输出

```
✅ 管道已通: Python/pytest + GitHub Actions + 两段冒烟 + 增量基线84%
→ PHASE→testing → 回coding-max
```

## 硬约束

1. 不写业务测试
2. Phase1=静态检查，不装依赖
3. Phase2才装依赖跑验证
4. 不装全局CLI(pip/npm install框架除外)
5. CI跑通再提交
6. 增量覆盖率，不卡全局%
7. 已有框架不重复装
8. 已有CI不覆盖(补缺失平台)
9. Python/Node/Go/Rust/Java一等支持，其他通用模板
10. 审计用文件工具不用shell
11. Monorepo子包独立审计
12. CI含缓存+覆盖率上传步骤

## 参考

- `references/smoke-templates.md` — Phase1模板(Python/Node/Go/Rust/Java)
- `references/gitlab-ci-template.yml` — GitLab CI两阶段
- `references/universal-ci-template.yml` — 通用Docker+Bash模板
- `../coding-max` — 配套: 根因修复引擎
