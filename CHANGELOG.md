# Changelog

> 自 `v0.1.3beta` 起重新建立 Beta 版本线。仓库既有 `v1.0.0`、`v1.0.2`、`v2.0.0` 标签作为早期历史快照保留，不移动、不覆盖。

## [0.1.3beta] - 2026-07-15

### coding-max

- 新增按需高级诊断层：反向数据流溯源、偶现分类、不可信诊断输入、性能与资源路由。
- 明确 origin 与传播点的区别，要求证明契约首次被破坏的位置。
- 保持单 Agent 与平台无关，不绑定特定模型、宿主产品或工具协议。
- `SKILL.md` 保持轻量，并新增 4 KiB 入口体积契约。

### 文档与验证

- 同步 README、贡献指南和全部示例到当前 Explore/Review/Quick/Standard/Hotfix 工作流。
- 新增机器可读 `VERSION`，并以契约测试防止版本与公开文档漂移。
- 继续使用 Bug、Review、Pipeline 报告及索引闭环；本地项目记忆不进入发布包。

## 历史快照

### [2.0.0] - 2026-07-12

- 从单一 `coding-max` 扩展为 `coding-max` + `coding-pipeline` 双 Skill。
- 新增测试荒漠审计、测试框架建立、CI 模板和 PHASE 联动原型。

### [1.0.2] - 2026-07-12

- 精炼根因修复流程、模式路由、TDD、自审、插桩和 Hotfix 约束。
- 扩充 Python、Node.js、Go、Rust、Java 的测试与 CI 参考。
- 修复 description 泄露内部工作流、合法语法误判和悬空引用。

### [1.0.0] - 2026-07-12

- 初始发布 `coding-max`。
- 提供 Explore、Quick、Standard、Hotfix 修复模式。
- 引入 RED→GREEN、根因分析、项目病历和断点恢复工作流。
