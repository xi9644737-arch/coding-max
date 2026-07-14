# Pipeline 执行契约

## 1. 审计

排除 `.git/node_modules/.venv/venv/vendor/target/build/dist` 和缓存。逐包检查框架、本地命令、CI、覆盖率、pre-commit：S0无测试、S1有本地测试、S2有CI、S3有覆盖率+稳定性监控。只增量修改已有能力。仅平台、依赖源、通知等选择影响结果时等待确认。

默认框架：Python=`pytest+pytest-cov`；Node/TS 沿用现有（Vite优先Vitest）；Go=标准库`testing`；Rust=`cargo test`；Java/Kotlin=`JUnit5+JaCoCo`。不引入非必要框架。

## 2. 三层预检

1. 静态不装包：Python `ast.parse`、JS `node --check`、配置语法。无本地 TS 编译器时只查文件和相对 import，不宣称类型通过。
2. 工具链：`go vet/build`、`cargo check/clippy`、`mvn/gradle compile`；如实记录依赖解析。
3. 恢复依赖后运行最小测试，以真实非零退出码为准；文件存在、空断言、`console.assert` 不能作 gate。

## 3. CI 与覆盖率

检测默认分支和既有 workflow；按真实目录、命令、运行时和依赖文件改写平台 reference。缓存优先 lockfile；没有则绑定 manifest 并记录非锁定风险。Monorepo 用独立 job/显式矩阵。生成后清占位和假通过命令并验证语法。

Codecov、Slack、pre-commit 仅在已有配置或授权时加。CI runner 可装获授权且锁版本的工具，不改用户全局环境。覆盖率无可靠来源写 `unknown`，不得估算。

## 4. 状态与报告

PHASE 写 `target/skill/timestamps/retry/verification_level/report`。报告前后成熟度、逐包结果、修改文件、真实命令/退出码、覆盖率来源、验证层级、风险和回滚。远程未运行写“待验证”；三次失败写 `failed`，不得用占位脚本标完成。
