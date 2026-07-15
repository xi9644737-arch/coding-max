---
name: coding-untangle
description: Audit and untangle structural coupling in existing codebases. Use for circular dependencies, wrong-layer logic, shared mutable state, duplicated contracts, temporal or change coupling, god modules, unsafe refactors, dependency-boundary recovery, or architecture fitness rules.
---

# coding-untangle

用行为证据证明耦合，以可逆迁移恢复既有项目边界。

## 路由

- **Explore**：只读审计依赖、状态、时序与变更耦合；读取 `references/coupling-audit.md`，不改代码或病历。
- **Guard**：实现前确认契约/状态所有者、允许的依赖方向和最小边界；同读 audit。
- **Untangle**：确认耦合造成行为或维护风险后，读取 `references/safe-untangling.md`，先保护行为，再逐调用方迁移。
- **Vaccine**：已确认目标边界后读取 `references/fitness-rules.md`；需补测试/CI 时调用 `../coding-pipeline/SKILL.md`。

## 协作边界

任务根按用户目录 > 最近 manifest/config > Git 根；不得污染父仓库。由 `coding-max` 发现结构性根因时，沿用其活动 Bug/Review 和范围；本 Skill 不得关闭原 Bug，完成后返回 `../coding-max/SKILL.md` 验证症状、影响面与最终 Review。显式只读仅在回复中交付；获授权的独立审计写 Review，确认缺陷仍用 coding-max 病历格式。

Pipeline 只实现已经定义的规则，不决定分层、接口或状态所有权。本 Skill 不搭测试框架、不配置通用 CI，不扩张为新项目设计、功能规划、技术选型或 Agent Harness。

## 核心流程

1. 证明耦合：以改动半径、重复缺陷、逆向依赖、顺序敏感、共享状态或不可独立验证为证据；指标只生成假设。
2. 锁定行为：建立 characterization/contract test；无可信入口时先交 pipeline。
3. 定义目标：写清规则/状态所有者、允许方向、最小 seam、保持行为和回滚点。
4. 增量迁移：一次迁移一个强相关调用方并验证；不得并行保留无退出条件的双路径。
5. 收口：删除旧实现、重复契约、临时 wrapper、死代码与 debug；验证原行为、边界和依赖方向。

## 完成条件

行为保护和相关测试通过；目标依赖方向可验证；未新增循环、重复规则或所有权不明的共享状态；旧路径已删除，或记录明确退出条件与剩余风险。被 coding-max 调用时只报告结构修复证据并交回，不冒充原缺陷已解决。

## 硬约束

不做无保护的大爆炸重写；不为假想复用造抽象；不以层数、import 数或复杂度单独定罪；不把兼容层当终态；不改变未获授权的公开契约或持久化格式；不绑定 Agent、模型、IDE、MCP 或厂商；不擅自提交、推送或安装全局工具。

## 按需资源

- 证据、分类、范围和误报：`references/coupling-audit.md`
- 行为保护、seam、迁移和收口：`references/safe-untangling.md`
- 架构测试、lint 与 CI 疫苗：`references/fitness-rules.md`
