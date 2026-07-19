# 项目病历与状态格式

统一写任务根 `.project-memory/`，从 `memory-template/` 按需补缺；不覆盖旧内容或并建等价记忆。`PHASE.json` 仅用于 pipeline，`.resume.md` 仅用于阻塞。

## Bug 病历

路径：`.project-memory/bugs/BUG-YYYY-MM-DD-<slug>.md`。

```markdown
---
id: BUG-YYYY-MM-DD-<slug>
status: investigating
diagnosis_stage: unknown
mode: quick | standard
urgency: routine | hotfix
risk:
  blast_radius: low | medium | high
  uncertainty: low | medium | high
  irreversibility: low | medium | high
  migration: none | present
  security: none | present
  data: none | present
  public_contract: none | present
human_gate:
  required: false
  reason: null
  decision_needed: null
actionability:
  decision: pending | passed
  evidence: []
  blockers: []
signature:
  component: null
  failure_mode: null
  origin_contract: null
  symptom_fingerprint: null
  environment: null
history_retrieval:
  status: pending | matched | no-match | unavailable
  patterns: []
  cases: []
  hypotheses: []
  checks: []
stage_evidence: []
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

`stage_evidence` 写 `{stage, evidence}`；证据须可复核。未知字段保留 `null`，随当前证据补齐，不得从历史复制为事实。`history_retrieval` 只记录实际检索、假设和待验证检查。

## 交叉不变量

- 生命周期为 `investigating -> fixing -> verifying -> resolved`；任一活动状态可进入 `blocked`，恢复时回到记录的活动状态。
- `diagnosis_stage` 只按 incident protocol 推进或回退，与生命周期正交。永久修复进入 `fixing` 前，`actionability.decision` 必须为 `passed`、证据非空且无待决 Human Gate；预授权可逆止血须标为止血，不冒充永久修复。
- `resolved` 仅允许同时满足：`diagnosis_stage: regression-proven`、验证表含实际执行结果、`resolved` 为真实日期。`blocked` 必须记录阻塞证据、下一步和 `.resume.md`；不得写关闭日期。
- 不得以摘要替代命令或把未运行检查标为通过。RED 须落在产品断言；harness 问题先修设施，只记录改变调查方向的被拒证据。
- 现象病历持有影响与产品 RED，根因病历持有上游证据；互链但不得重复认领 RED、修复或验证。
- 回滚不得删除或弱化回归疫苗；API 回退时改为旧合同防复活门。引用只填已观察到的 commit/PR/release，不得为填字段擅自提交；测试存在不等于 CI 已执行。
- 仅生产问题或 Hotfix 写真实观察指标。Hotfix 可事后建档，但须区分可逆止血与 Standard 永久修复。

## Review

路径：`.project-memory/reviews/REVIEW-YYYY-MM-DD-<slug>.md`。

```markdown
---
id: REVIEW-YYYY-MM-DD-<slug>
status: reviewing | completed | blocked
reviewed: YYYY-MM-DD
scope: working-tree | commit | branch | files
---
# <标题>
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

`REVIEWS.md` 索引列为日期、状态、范围、发现数、已修复、报告。零发现也关闭；每个实际修复问题链接独立 Bug 病历。

## PHASE、恢复与疫苗

`PHASE.json` 保留 `state,target,skill,started_at,updated_at,retry,verification_level,report`，合法流转为 `idle -> bootstrapping -> testing -> done|failed`。本地成功写 `local`；仅观察到远程 CI 成功才写 `remote`。

三次失败写 `failed`、`retry: 3` 和报告路径，再从 `RESUME.md` 创建 `.resume.md`，记录阻塞证据、事实、下一步、次数和恢复命令；解决后删除。标签用小写 kebab-case。疫苗优先复用现有 lint、类型、测试或 CI，不为单一病例引入重依赖。
