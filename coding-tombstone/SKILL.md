---
name: coding-tombstone
description: Prove and safely retire obsolete code, compatibility paths, flags, assets, tests, configs, and release residue in existing projects. Use before beta or public releases, after migrations, or when deprecated and dead paths must be removed without resurrection.
---

# coding-tombstone

证明死亡，安全退役，留下阻止旧路径复活的墓碑。

## 路由

- **Audit**：读取 `references/retirement-workflow.md`，只读分类候选。
- **Mark**：证据不足或需兼容窗口时写 `candidate|deprecated|blocked`。
- **Retire**：获授权后再读 `references/tombstone-format.md`，分批删除并验证。
- **Release sweep**：发布前审计旧入口、兼容、flag、迁移物、debug 和公开表面；不发布。

## 所有权

任务根按用户目录 > 最近 manifest/config > Git 根；不得污染父仓库。显式只读只在回复交付。获授权后写 `.project-memory/tombstones/` 与 `TOMBSTONES.md`，已有等价记录则沿用。

只拥有“证明废弃→退役→防复活”。Bug 交 `../coding-max/SKILL.md`，结构边界交 `../coding-untangle/SKILL.md`，验证荒漠交 `../coding-pipeline/SKILL.md`。coding-max 终审，本 Skill 维护墓碑。

## 核心流程

1. 冻结范围/dirty baseline；分类 safe-delete、deprecate、retain、blocked。
2. 证明替代物与静态、动态、配置、构建、公开和数据消费者。
3. 先保护替代行为与非 happy path；无证据不删。
4. 一次退役一个可回滚集合，清引用/测试/文档/配置和双路径。
5. 做恢复反事实，运行相关测试、构建、打包与残留搜索。
6. 写墓碑/索引；仅真实证据写 `verified`，否则 `blocked`。

## 完成条件

替代物、消费者、删除、验证、回滚和版本可追溯；公开 API/数据格式已兼容退役或获授权；仅按已有 formatter/linter 机械统一；无临时 wrapper、旧合同或墓碑外副本。

## 硬约束

不以零引用、覆盖率、年龄或复杂度单独判死；不移入 `.attic`/graveyard/备份冒充删除；不主观全仓改写；不删未知生成物、迁移、许可证或用户数据；不擅自 commit/push/发布；不绑定 Agent、模型、IDE、MCP 或厂商。

## 按需资源

- 盘点、证明、兼容窗口、分批删除与发布验证：`references/retirement-workflow.md`
- 墓碑生命周期、模板与索引：`references/tombstone-format.md`
