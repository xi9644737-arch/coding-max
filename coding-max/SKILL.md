---
name: coding-max
description: 修复软件缺陷、排查异常、定位根因、处理 hotfix、验证修复，或在实现完成后审查代码并修复确认的问题。用户提到修 bug、fix、debug、报错、崩溃、线上故障、根因分析、代码审查、质量检查或验证修复时使用。
---

# coding-max

用证据定位根因，以测试约束修复，并把实际改动沉淀为可检索病历。

## 路由

- **Explore**：只诊断，不改代码或项目记忆。读取 `references/repair-workflow.md` 的诊断部分。
- **Review**：审查实现/diff；未授权修复则只报告。读取 `references/patch-signals.md`；需落盘再读病历格式。
- **Trivial/Quick**：文案格式类/单模块小影响；Quick 默认。读取 repair workflow；改代码必须读病历格式。
- **Standard**：并发、多模块、架构或高风险；同上，并完整执行影响面/Premortem。
- **Hotfix**：线上紧急；先止血验证，事后补 `[HOTFIX]` 病历。

“修复后终审”走 Quick/Standard→Review；实现已完成直接 Review。范围外旧问题只记风险，除非用户授权扩大。

## 任务边界

任务根优先级：用户明确目录 > 最近 manifest/config > Git 根；不得污染无关父仓库。统一写任务根 `.project-memory/`。从 `memory-template/` 初始化缺项，不覆盖旧内容。仓库指令要求沉淀即视为授权，否则首次创建前询问；显式只读时只在回复中按同结构交付。

Review 先看目标 diff，再查被改契约、调用方和测试，只报告影响行为、安全、数据或架构的确认问题。发现需修复的缺陷，切 Quick/Standard 完成后回 Review。

## 完成条件

所有实际代码改动必须有 RED/可重复失败证据、根因、最小修复、相关验证和已关闭 Bug 报告；通过写 `resolved`，未解写 `blocked`，并更新 `BUG_PATTERNS.md`。Review 写范围、发现/处置、验证、剩余风险，更新 `REVIEWS.md`。仅联动 pipeline 时使用 `.project-memory/PHASE.json`。

不得把无关既有失败算成本次回归或声称全量通过；连续三次当前修复失败时写 `.resume.md` 并硬停。最后清理 trace、临时测试/日志和完成的恢复点。

## 硬约束

RED 先于 GREEN；异常须处理/传播/记录上下文；不把假设当根因，不伪造命令、覆盖率或 CI；不越界重构，不做未授权 push、全局安装或破坏操作。单 Agent 完整执行，不依赖子代理、特定模型或 MCP。

## 按需资源

- 诊断、影响面、TDD、验证、关闭：`references/repair-workflow.md`
- Review/Premortem/架构信号：`references/patch-signals.md`
- 病历/Review/PHASE/恢复格式：`references/bug-memory-format.md`
- 初始化：`memory-template/`
- 测试荒漠：`../coding-pipeline/SKILL.md`
