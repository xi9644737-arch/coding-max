# 项目病历与状态格式

## 目录

1. 初始化规则
2. Bug 报告生命周期
3. Bug 索引与模式合并
4. Review 报告与索引
5. PHASE 状态协议
6. 恢复点
7. 标签与疫苗

## 1. 初始化规则

统一写入项目根 `.project-memory/`；按需创建 `bugs/`、`reviews/`、`pipelines/`、`BUG_PATTERNS.md`、`REVIEWS.md`、`PROJECT_PROFILE.md` 和 `PHASE.json`，不覆盖已有内容。

优先复制 `memory-template/`。仅在阻塞时把 `RESUME.md` 复制为 `.project-memory/.resume.md`；`PHASE.json` 仅在联动 pipeline 时创建。若仓库已有等价项目记忆，沿用其路径并注明，不并行创建第二套。

## 2. Bug 报告生命周期

路径：`.project-memory/bugs/BUG-YYYY-MM-DD-<slug>.md`。

状态：

```text
investigating -> fixing -> verifying -> resolved
                                  \-> blocked
```

```markdown
---
id: BUG-YYYY-MM-DD-<slug>
status: investigating
severity: trivial | quick | standard | hotfix
reported: YYYY-MM-DD
resolved: null
tags: []
---

# <标题>

## 症状与影响
- 症状：
- 影响范围：
- 环境：

## 最小复现
- 命令或步骤：
- 预期：
- 实际：
- RED 证据：

## 根因
- 直接原因：
- Why 1：
- Why 2：
- 同模式扫描：
- 关联病历：无 | 现象: BUG-... | 根因: BUG-...

## 修复
- 方案：
- 修改文件：
- 契约变化：无 | <说明>
- 回滚：

## 验证
| 命令 | 结果 | 证据摘要 |
|---|---|---|

## 闭环
- 关联变更：未提交 | <commit / PR / release>
- 回归疫苗：<测试、lint、类型检查或 CI gate>
- 自动执行：本地默认测试 | <CI job> | 尚未接入
- 上线观察：不适用 | <指标、窗口、阈值>

## 胶囊
- 弯路：
- 突破：
- 下次优先检查：
```

规则：

- 修改前写 `investigating`，开始修改写 `fixing`，运行最终验证写 `verifying`。
- 验证通过写 `resolved` 和真实日期；不能解决写 `blocked`、阻塞证据和下一步。
- 不得以摘要替代实际命令，不得把未运行的检查标为通过。
- RED 须落在产品断言；barrier、timeout、fixture、清理或钩子失败先修 harness。只把改变方向的被拒证据写入“弯路”，不记操作错误。
- 多病历链中，现象病历持有用户影响与产品 RED，根因病历持有上游合同/结构证据；互链但不得重复认领同一 RED、修复或验证，独立根因独立关闭。
- 修复须写回归疫苗及是否进入默认测试/CI；测试存在不等于 CI 已执行。
- 回滚不得删除或弱化回归疫苗；新 API 被回退时把疫苗改写为旧合同防复活门，无法保留须说明。
- 关联变更只填已观察到的 commit、PR 或 release；未提交照实写，不得为填字段擅自提交或伪造引用。
- 上线观察仅在生产问题、Hotfix 或用户要求时填写指标、窗口和阈值；其他任务写“不适用”，不得虚构生产环境。
- Hotfix 可以事后创建，但必须写 `[HOTFIX]` 标签和止血/永久修复差异。

## 3. Bug 索引与模式合并

`BUG_PATTERNS.md` 索引：

```markdown
| 日期 | 状态 | 类型 | 标签 | 症状摘要 | 报告 |
|---|---|---|---|---|---|
| 2026-07-14 | resolved | quick | null-check | 缺失字段导致崩溃 | [BUG-...](bugs/BUG-....md) |
```

索引下记录可复用模式。根因标签和关键症状至少两项匹配时合并，不重复创建同一模式；在原模式追加本次报告链接和差异。只相似但根因未证实时新建条目。

## 4. Review 报告与索引

路径：`.project-memory/reviews/REVIEW-YYYY-MM-DD-<slug>.md`。

```markdown
---
id: REVIEW-YYYY-MM-DD-<slug>
status: reviewing | completed | blocked
reviewed: YYYY-MM-DD
scope: working-tree | commit | branch | files
---

# <审查标题>

## 范围
- 基线：
- 文件：
- 审查标准：

## 发现与处置
| 严重度 | 发现 | 证据 | 处置 | Bug 报告 |
|---|---|---|---|---|

## 验证
| 命令 | 结果 |
|---|---|

## 剩余风险
- 无 | <说明>
```

`REVIEWS.md` 使用：

```markdown
| 日期 | 状态 | 范围 | 发现数 | 已修复 | 报告 |
|---|---|---|---:|---:|---|
```

没有确认问题时也关闭 review 报告，发现数写 0。每个实际修复的问题必须链接独立 Bug 报告，避免把多个根因塞入一份审查记录。

## 5. PHASE 状态协议

路径：`.project-memory/PHASE.json`。

从 `memory-template/PHASE.json` 初始化；保留 `state`、`target`、`skill`、时间、`retry`、`verification_level` 和 `report` 字段。

合法流转：

```text
idle -> bootstrapping -> testing -> done
                         \-> failed
```

- `coding-max` 发现测试荒漠时写 `bootstrapping` 并交给 `coding-pipeline`。
- `coding-pipeline` 让本地测试可执行后写 `testing`。
- 本地验证完成写 `done`、`verification_level: local`。
- 只有实际看到远程 CI 成功才写 `verification_level: remote`。
- 三次失败写 `failed`，`retry: 3`，并填写报告路径。

## 6. 恢复点

三次失败或外部阻塞时把 `memory-template/RESUME.md` 复制为 `.project-memory/.resume.md`，填写工作、模式、步骤、次数、视角、时间，以及已证实/排除/待验证事实和恢复命令。

恢复前核对工作树；解决后删恢复点。

## 7. 标签与疫苗

标签用小写 kebab-case，如 `race-condition`、`memory-leak`、`boundary`、`wrong-layer`。

同一架构标签累计三次时提示独立重构。疫苗优先选择能自动阻断同类问题的 lint、类型检查、测试或 CI 规则；新增工具前评估项目现有生态，不为一条病历强行引入重依赖。
