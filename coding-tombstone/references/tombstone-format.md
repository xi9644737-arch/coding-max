# 墓碑格式

统一写入 `.project-memory/tombstones/TOMBSTONE-YYYY-MM-DD-<slug>.md`，并更新 `.project-memory/TOMBSTONES.md`。不覆盖旧记录；同一退役集合沿用一份墓碑。

状态只使用：

```text
candidate -> deprecated -> removed -> verified
任一活动状态 -----------------------> blocked
```

```markdown
---
id: TOMBSTONE-YYYY-MM-DD-<slug>
status: candidate
target_release: unknown
created: YYYY-MM-DD
verified: null
tags: []
---

# <退役集合>

## 候选与替代
- 退役对象：<文件、符号、入口、协议、配置或资产>
- 原所有者：
- 替代物：none | <路径/合同>
- 排除范围：

## 死亡证明
- 静态消费者：
- 动态/配置/构建消费者：
- 公开 API 与持久化：
- 反事实：

## 退役
- 删除范围：
- 保留内容及原因：
- 兼容窗口/退出条件：不适用 | <说明>
- 回滚：

## 验证
| 命令 | 结果 | 证据摘要 |
|---|---|---|

## 闭环
- 关联变更：未提交 | <commit / PR / release>
- 防复活门禁：<测试、lint、搜索或构建规则>
- 自动执行：<默认测试 / CI job / 尚未接入>
- 剩余风险：无 | <说明>

## 胶囊
- 误判候选：
- 删除突破：
- 下次优先检查：
```

规则：

- `candidate` 只表示待证，不等于可删；需要窗口写 `deprecated`。
- 开始删除写 `removed`；验证完成才写 `verified` 和真实日期。
- 任一活动状态无法证明或验证失败都写 `blocked`、证据和退出条件，不留虚假进行态。
- 一个墓碑覆盖一个可独立回滚的强相关集合；独立根因/替代物应拆分。
- 关联变更只填已观察值，不为填表擅自提交；远程 CI 未观察不得写通过。
- `TOMBSTONES.md` 只索引事实，不复制全文：

```markdown
| 日期 | 状态 | 目标版本 | 对象 | 替代物 | 墓碑 |
|---|---|---|---|---|---|
```
