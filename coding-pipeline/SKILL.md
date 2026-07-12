# coding-pipeline

> **触发**: "搭测试"/"配CI"/"加覆盖率"/"没有测试"/"搭流水线"
> 只通管道不写业务测试。CI能跑+冒烟通过+增量基线有=完工。业务测试留给coding-max。

## 联动
coding-max步骤8无测试→本skill→完工写`.pipeline-done`→回coding-max。可独立召唤。

`.pipeline-done`格式: `ok:<框架>,CI=<平台>,baseline=<N>%`。coding-max读此文件确认管道就绪。

## 流程

### 0.审计(用文件工具，不用终端)
递归Monorepo子包。输出间隙表:
| 检查项 | 状态 | 行动 |
|--------|------|------|
| 测试框架 | ✅/⚠️/❌ | 装/补配置/— |
| CI(GitHub) | ✅/❌ | 生成test.yml |
| CI(GitLab) | ✅/❌ | 生成.gitlab-ci.yml |
| 覆盖率上报 | ✅/❌ | CI加Codecov |
| Pre-commit | ✅/❌ | 问 |
⚠️=有框架缺插件。成熟度:**S0**荒漠→**S1**有框架→**S2**有CI→**S3**全有+监控。间隙表指明当前级和缺什么。

### 1.装框架(S0/⚠️)
| 语言 | 检测 | 框架 | Phase1 |
|------|------|------|--------|
| Python | pyproject.toml/setup.cfg | pytest+pytest-cov | ast.parse+裸except+可变默认 |
| Node/TS | package.json | vitest/jest | 入口+裸catch+import |
| Go | go.mod | testing+testify | go vet+go build |
| Rust | Cargo.toml | cargo test+llvm-cov | cargo check+clippy |
| Java | pom.xml/build.gradle | JUnit5+JaCoCo | mvn/gradle compile |
其他→`references/universal-ci-template.yml`

### 2.两阶段冒烟
**Phase1**(秒级，不装依赖):上表Phase1列。失败→跳Phase2。
**Phase2**:Phase1通过→装依赖→跑脚手架(能跑即可)。模板见`references/smoke-templates.md`

### 3.生成CI
无CI→生成`.github/workflows/test.yml`(默认)/`.gitlab-ci.yml`。Monorepo→子包独立job。含:版本矩阵、缓存、Phase1→2依赖、Codecov、Slack(可选)。

### 4.增量基线+Pre-commit
`git diff HEAD~1`→只算变更文件新增行。写入PROJECT_PROFILE。coding-max步骤8只比增量≥基线。
Pre-commit:探测`.pre-commit-config.yaml`→有则追加测试;无则问→推荐ruff+pytest(Python)/lint-staged+vitest(Node)。

### 5.完工
写`.pipeline-done`:`ok:<框架>,CI=<平台>,baseline=<N>%`。通知coding-max管道就绪。

## 硬约束
1.不写业务测试 2.Phase1不装依赖 3.Phase2才装 4.不装全局CLI 5.CI跑通+写.pipeline-done再提交 6.增量不卡全局% 7.已有不重复 8.已有CI不覆盖 9.Python/Node/Go/Rust/Java一等 10.审计用文件工具 11.Monorepo子包独立 12.CI含缓存+覆盖率

## 参考
`references/smoke-templates.md` | `references/gitlab-ci-template.yml` | `references/universal-ci-template.yml` | `../coding-max`
