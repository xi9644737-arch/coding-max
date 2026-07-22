# 历史病例检索协议

修复模式在 `failure-confirmed` 后、`localized` 前执行一次。历史只提出待证伪假设，不是当前证据。无索引或不可读时写 `unavailable`，不得扩大扫描。

## 检索与回写

1. 当前病历先记录症状并补可证实的 `signature`；未知保持 `null`，不得从历史复制。
2. 只读 `BUG_PATTERNS.md` 索引和模式块，不遍历全部病历。忽略含 `null` 的比较，按首个命中层取候选：
   - A：`origin_contract` + `failure_mode`；
   - B：`component` + `failure_mode`；
   - C：`symptom_fingerprint` + `environment`。
3. 同层按五字段命中数、病例日期、pattern ID 排序，只完整加载前 1–3 个不同病例。
4. 结构化零命中时兼容旧索引：根因标签交集至少两项，且症状摘要指向同一对象与失败结果，才可列为低置信候选；不得据此合并模式或补写 signature。
5. 写回 `history_retrieval`：`status: matched | no-match | unavailable`，以及实际读取的 `patterns/cases`、新增的 `hypotheses` 和待执行 `checks`。零命中继续独立调查。

历史材料只能新增可证伪假设和检查项，不能单独推进 `localized`、`cause-confirmed`、Actionability Gate 或关闭。采用项必须由当前代码、产品 RED 或因果实验验证；冲突时以当前证据为准。

## 合并与反馈

达到 `cause-confirmed` 后才评估合并。仅当前证据确认相同 `origin_contract` 与 `failure_mode` 且其余 signature 不矛盾时，追加病例与差异；否则新建 stable ID。

同根因第二次，或 security/data/public_contract 硬风险一次，标 `prevention_status: candidate`；第三次复发改 `failed` 并提出 invariant test、CI gate 或架构治理。Detection/Prevention 必须链接当前证据。
