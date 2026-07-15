# Bug Patterns

## 病例索引

| 日期 | 状态 | Mode | Urgency | Component | Failure mode | 症状摘要 | 报告 |
|---|---|---|---|---|---|---|---|

## 可复用模式

```yaml
id: PATTERN-<stable-id>
component: <normalized-id>
failure_mode: <normalized-id>
origin_contract: <normalized-id>
symptom_fingerprint: <normalized-id>
environment: <normalized-id | any>
root_cause_tags: []
prevention_status: candidate | active | failed
```

- Detection：<当前可复核信号或检查>
- Prevention：<测试、invariant、lint 或 CI gate>
- Cases：<BUG 链接及本次差异>

<!-- 每个模式复制一份完整块；字段未知时写 null，不猜测。检索与合并遵循 references/memory-retrieval.md。 -->
