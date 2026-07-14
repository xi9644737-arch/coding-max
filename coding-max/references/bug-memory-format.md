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

统一写入项目根目录的 `.project-memory/`。创建缺失目录和文件，不覆盖已有内容：

```text
.project-memory/
├── BUG_PATTERNS.md
├── REVIEWS.md
├── PROJECT_PROFILE.md
├── PHASE.json
├── bugs/
├── reviews/
└── pipelines/
```

优先复制 `memory-template/`。仅在阻塞时把 `RESUME.md` 复制为 `.project-memory/.resume.md`；`PHASE.json` 仅在联动 pipeline 时创建。若仓库已有等价项目记忆，沿用其路径并注明，不并行创建第二套。

## 2. Bug 报告生命周期

路径：`.project-memory/bugs/BUG-YYYY-MM-DD-<slug>.md`。

状态只使用：

```text
investigating -> fixing -> verifying -> resolved
                                  \-> blocked
```

报告模板：

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

## 修复
- 方案：
- 修改文件：
- 契约变化：无 | <说明>
- 回滚：

## 验证
| 命令 | 结果 | 证据摘要 |
|---|---|---|

## 胶囊
- 弯路：
- 突破：
- 下次优先检查：
```

规则：

- 修改前写 `investigating`，开始修改写 `fixing`，运行最终验证写 `verifying`。
- 验证通过写 `resolved` 和真实日期；不能解决写 `blocked`、阻塞证据和下一步。
- 不得以摘要替代实际命令，不得把未运行的检查标为通过。
- Hotfix 可以事后创建，但必须写 `[HOTFIX]` 标签和止血/永久修复差异。

## 3. Bug 索引与模式合并

`BUG_PATTERNS.md` 顶部索引：

```markdown
| 日期 | 状态 | 类型 | 标签 | 症状摘要 | 报告 |
|---|---|---|---|---|---|
| 2026-07-14 | resolved | quick | null-check | 缺失字段导致崩溃 | [BUG-...](bugs/BUG-....md) |
```

索引下面记录可复用模式。根因标签和关键症状至少两项匹配时合并，不重复创建同一模式；在原模式追加本次报告链接和差异。只相似但根因未证实时新建条目。

常用同义扩展：

| 症状 | 同义词 |
|---|---|
| 崩溃 | crash, panic, segfault, 闪退 |
| 卡住 | hang, freeze, deadlock, timeout |
| 偶发 | flaky, intermittent, race, heisenbug |
| 数据错误 | corruption, stale, data loss, wrong result |
| 不生效 | no-op, precedence, cache invalidation |
| 回归 | regression, upgrade, downgrade, bisect |

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

```json
{
  "state": "idle",
  "target": "",
  "skill": "coding-max",
  "started_at": null,
  "updated_at": null,
  "retry": 0,
  "verification_level": "none",
  "report": null
}
```

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

旧 `.pipeline-done` 只用于一次性迁移读取；读取后转换为 `PHASE.json`，不再继续生成。

## 6. 恢复点

路径：`.project-memory/.resume.md`。三次失败或外部阻塞时写：

```yaml
---
work_id: BUG-YYYY-MM-DD-<slug>
mode: quick | standard | review | hotfix
step: reproduce | diagnose | fix | verify | report
strikes: 3
perspective: data-flow | call-chain | config | timing
blocked_at: <ISO-8601>
---

## 已验证事实

## 已排除假设

## 待验证假设

## 恢复命令
```

恢复时先验证工作树和报告仍对应当前代码，再继续；解决后删除恢复点。

## 7. 标签与疫苗

标签保持小写 kebab-case：

- 异常：`swallowed-exception`, `type-error`, `null-check`
- 并发：`race-condition`, `deadlock`, `thread-safety`
- 资源：`memory-leak`, `connection-leak`, `file-not-closed`
- 输入：`sql-injection`, `xss`, `path-traversal`, `no-validation`
- 逻辑：`off-by-one`, `boundary`, `infinite-loop`
- 架构：`arch-coupling`, `circular-import`, `wrong-layer`, `god-module`

同一架构标签累计三次时提示独立重构。疫苗优先选择能自动阻断同类问题的 lint、类型检查、测试或 CI 规则；新增工具前评估项目现有生态，不为一条病历强行引入重依赖。
