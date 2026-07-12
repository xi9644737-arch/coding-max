---
name: coding-pipeline
description: 搭测试管道。触发:搭测试/配CI/加覆盖率/测试基建/github actions/monorepo。只通管道不写业务测试。
---

# coding-pipeline

**只通管道，不写业务测试。** CI能跑+冒烟通过+增量基线有=完工。业务测试留给 `coding-max` 修bug时填。

## 联动

coding-max步骤8无测试→`PHASE.json(state:bootstrapping)`→本skill→`state:testing`→回coding-max。也可独立召唤。

## 流程

### 0. 审计 (Glob/Grep/Read)

递归Monorepo子包。输出**间隙表**:

| 检查项 | 状态 | 行动 |
|--------|------|------|
| 测试框架 | ✅/⚠️/❌ | 装框架 / 补配置 / — |
| CI(GitHub) | ✅/❌ | 生成 `.github/workflows/test.yml` |
| CI(GitLab) | ✅/❌ | 生成 `.gitlab-ci.yml` |
| 覆盖率上报 | ✅/❌ | CI加Codecov action |
| Pre-commit | ✅/❌ | 问是否配置 |

⚠️=框架装了但缺插件(有pytest无pytest-cov)。

成熟度: **S0**测试荒漠 → **S1**有框架 → **S2**有CI → **S3**全有+监控。间隙表指明当前级和缺什么。

### 1. 装框架 (S0/⚠️时)

| 语言 | 检测文件 | 框架 | Phase1 |
|------|---------|------|--------|
| Python | `pyproject.toml`/`setup.cfg` | pytest+pytest-cov | `ast.parse`+裸except+可变默认 |
| Node/TS | `package.json` | vitest(Vite)/jest | 入口+裸catch+import可解析 |
| Go | `go.mod` | testing+testify | `go vet`+`go build` |
| Rust | `Cargo.toml` | cargo test+llvm-cov | `cargo check`+`cargo clippy -D warnings` |
| Java | `pom.xml`/`build.gradle` | JUnit5+JaCoCo | `mvn compile`/`gradle compileJava` |

其他语言→`references/universal-ci-template.yml`。

### 2. 两阶段冒烟

**Phase1** (秒级，不装依赖): 上表Phase1列。失败→跳过Phase2。

**Phase2**: Phase1通过→装依赖→跑脚手架(框架能跑即可，不写业务断言)。模板见 `references/smoke-templates.md`。

### 3. 生成CI

无已有CI→生成 `.github/workflows/test.yml`(默认)/`.gitlab-ci.yml`(用户指定)。Monorepo→每子包独立job。含: 版本矩阵、lock文件缓存(`actions/cache@v4`)、Phase1→2依赖(`needs`)、Codecov step、Slack通知(可选)。

### 4. 增量基线

`git diff HEAD~1 --name-only`→只算变更文件新增/修改行。写入 `PROJECT_PROFILE`。coding-max步骤8只比增量≥基线。

## 硬约束

1. 不写业务测试 2. Phase1不装依赖 3. Phase2才装 4. 不装全局CLI 5. CI跑通再提交 6. 增量覆盖率不卡全局% 7. 已有不重复 8. 已有CI不覆盖 9. Python/Node/Go/Rust/Java一等 10. 审计用文件工具不用shell 11. Monorepo子包独立 12. CI含缓存+覆盖率step

## 参考

`references/smoke-templates.md` | `references/gitlab-ci-template.yml` | `references/universal-ci-template.yml` | `../coding-max`
